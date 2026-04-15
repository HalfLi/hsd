#!/usr/bin/env python3
"""
KRX triangle pattern scanner.

Scans KOSPI/KOSDAQ stocks for symmetric triangle / converging wedge candidates
using recent swing highs and lows. Outputs a CSV report and optional PNG charts.

Dependencies:
  pip install pykrx pandas numpy matplotlib scipy

Example:
  python triangle_scanner_krx.py --market KOSPI --top-n 20 --charts
  python triangle_scanner_krx.py --market ALL --max-tickers 300 --output-dir reports
"""
from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Iterable, List, Optional

import numpy as np
import pandas as pd

try:
    from scipy.signal import find_peaks  # type: ignore
except Exception:  # pragma: no cover
    find_peaks = None

try:
    import matplotlib.pyplot as plt
except Exception as e:  # pragma: no cover
    raise SystemExit("matplotlib 이 필요합니다. pip install matplotlib") from e

try:
    from pykrx import stock
except Exception as e:  # pragma: no cover
    raise SystemExit("pykrx 가 필요합니다. pip install pykrx") from e


@dataclass
class ScanConfig:
    market: str = "KOSPI"
    lookback_days: int = 90
    history_days: int = 180
    swing_window: int = 5
    min_touches: int = 3
    min_avg_volume: int = 150_000
    min_price: int = 2_000
    max_price: Optional[int] = None
    max_tickers: Optional[int] = None
    charts: bool = False
    top_n: int = 20
    output_dir: str = "triangle_reports"
    prominence_ratio: float = 0.018
    min_r2: float = 0.45
    max_days_to_apex: int = 25
    max_end_width_ratio: float = 0.65
    price_tolerance_ratio: float = 0.02
    volume_contract_ratio: float = 0.95


@dataclass
class ScanResult:
    ticker: str
    name: str
    score: float
    close: float
    upper_slope: float
    lower_slope: float
    upper_r2: float
    lower_r2: float
    start_width: float
    end_width: float
    end_width_ratio: float
    days_to_apex: float
    touch_highs: int
    touch_lows: int
    avg_volume_20d: float
    volume_contracting: bool
    last_date: str
    chart_path: Optional[str] = None


# ---------- data helpers ----------

def ensure_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def get_tickers(market: str) -> list[str]:
    market = market.upper()
    if market not in {"KOSPI", "KOSDAQ", "KONEX", "ALL"}:
        raise ValueError("market must be KOSPI / KOSDAQ / KONEX / ALL")
    return stock.get_market_ticker_list(market=market)


BAD_NAME_TOKENS = ("스팩", "SPAC", "리츠", "REIT", "ETF", "ETN")


def is_common_stock_name(name: str) -> bool:
    # 선호주/우선주, 스팩, ETF/ETN/리츠 제외
    if not name:
        return False
    if any(token in name.upper() for token in BAD_NAME_TOKENS):
        return False
    if name.endswith("우") or name.endswith("우B") or name.endswith("1우"):
        return False
    if "우(" in name:
        return False
    return True


# ---------- math helpers ----------

def linear_fit(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    if len(x) < 2:
        return math.nan, math.nan, -1.0
    m, b = np.polyfit(x, y, 1)
    y_hat = m * x + b
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(m), float(b), float(r2)


def line_value(m: float, b: float, x: float) -> float:
    return m * x + b


def clip(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


# ---------- extrema detection ----------

def _fallback_extrema(values: np.ndarray, order: int, kind: str) -> np.ndarray:
    idxs: list[int] = []
    for i in range(order, len(values) - order):
        window = values[i - order : i + order + 1]
        center = values[i]
        if np.isnan(center):
            continue
        if kind == "max":
            ok = center >= np.max(window)
        else:
            ok = center <= np.min(window)
        if not ok:
            continue
        if idxs and i - idxs[-1] <= order:
            prev = idxs[-1]
            replace = (values[i] > values[prev]) if kind == "max" else (values[i] < values[prev])
            if replace:
                idxs[-1] = i
        else:
            idxs.append(i)
    return np.array(idxs, dtype=int)


def find_swing_points(series: pd.Series, order: int, prominence: float, kind: str) -> np.ndarray:
    values = series.astype(float).to_numpy()
    if len(values) < order * 2 + 1:
        return np.array([], dtype=int)

    if find_peaks is not None:
        if kind == "max":
            idxs, _ = find_peaks(values, distance=order, prominence=prominence)
        else:
            idxs, _ = find_peaks(-values, distance=order, prominence=prominence)
        return np.array(idxs, dtype=int)

    return _fallback_extrema(values, order=order, kind=kind)


# ---------- core pattern logic ----------

def analyze_triangle(df: pd.DataFrame, cfg: ScanConfig) -> Optional[dict]:
    if df.empty or len(df) < cfg.lookback_days:
        return None

    recent = df.tail(cfg.lookback_days).copy()
    recent = recent[["시가", "고가", "저가", "종가", "거래량"]].astype(float)
    recent.reset_index(inplace=True)
    recent.rename(columns={"index": "날짜"}, inplace=True)
    recent["x"] = np.arange(len(recent), dtype=float)

    price_ref = float(recent["종가"].median())
    prominence = max(price_ref * cfg.prominence_ratio, 1.0)

    high_idx = find_swing_points(recent["고가"], order=cfg.swing_window, prominence=prominence, kind="max")
    low_idx = find_swing_points(recent["저가"], order=cfg.swing_window, prominence=prominence, kind="min")

    if len(high_idx) < cfg.min_touches or len(low_idx) < cfg.min_touches:
        return None

    high_idx = high_idx[-max(cfg.min_touches, 5) :]
    low_idx = low_idx[-max(cfg.min_touches, 5) :]

    xh = recent.loc[high_idx, "x"].to_numpy()
    yh = recent.loc[high_idx, "고가"].to_numpy()
    xl = recent.loc[low_idx, "x"].to_numpy()
    yl = recent.loc[low_idx, "저가"].to_numpy()

    m_high, b_high, r2_high = linear_fit(xh, yh)
    m_low, b_low, r2_low = linear_fit(xl, yl)

    if not np.isfinite([m_high, b_high, r2_high, m_low, b_low, r2_low]).all():
        return None

    # upper line falling, lower line rising = symmetric triangle / converging wedge
    if not (m_high < 0 and m_low > 0):
        return None
    if r2_high < cfg.min_r2 or r2_low < cfg.min_r2:
        return None

    x_start = float(max(xh.min(), xl.min()))
    x_now = float(recent["x"].iloc[-1])

    upper_start = line_value(m_high, b_high, x_start)
    lower_start = line_value(m_low, b_low, x_start)
    upper_now = line_value(m_high, b_high, x_now)
    lower_now = line_value(m_low, b_low, x_now)

    start_width = upper_start - lower_start
    end_width = upper_now - lower_now

    if start_width <= 0 or end_width <= 0:
        return None

    end_width_ratio = end_width / start_width
    if end_width_ratio > cfg.max_end_width_ratio:
        return None

    denom = (m_high - m_low)
    if abs(denom) < 1e-9:
        return None
    apex_x = (b_low - b_high) / denom
    days_to_apex = apex_x - x_now

    if not (0 <= days_to_apex <= cfg.max_days_to_apex):
        return None

    last_close = float(recent["종가"].iloc[-1])
    tolerance = last_close * cfg.price_tolerance_ratio

    # Price should still be inside the triangle or very near the line.
    if last_close > upper_now + tolerance:
        return None
    if last_close < lower_now - tolerance:
        return None

    # Touch validation: recent swing points should lie close to their fitted lines.
    high_line_vals = m_high * xh + b_high
    low_line_vals = m_low * xl + b_low
    high_err = np.abs(yh - high_line_vals) / np.maximum(yh, 1.0)
    low_err = np.abs(yl - low_line_vals) / np.maximum(yl, 1.0)

    high_touches = int(np.sum(high_err <= cfg.price_tolerance_ratio * 1.25))
    low_touches = int(np.sum(low_err <= cfg.price_tolerance_ratio * 1.25))
    if high_touches < cfg.min_touches or low_touches < cfg.min_touches:
        return None

    # Liquidity filters.
    avg_volume_20d = float(df["거래량"].tail(20).mean()) if len(df) >= 20 else float(df["거래량"].mean())
    if avg_volume_20d < cfg.min_avg_volume:
        return None
    if last_close < cfg.min_price:
        return None
    if cfg.max_price is not None and last_close > cfg.max_price:
        return None

    first_half = recent["거래량"].iloc[: len(recent) // 2].mean()
    second_half = recent["거래량"].iloc[len(recent) // 2 :].mean()
    volume_contracting = bool(second_half <= first_half * cfg.volume_contract_ratio) if first_half > 0 else False

    # Score: tighter squeeze, cleaner trendlines, more touches, nearer apex = higher.
    squeeze_score = clip(1.0 - end_width_ratio, 0.0, 1.0)
    quality_score = clip(min(r2_high, r2_low), 0.0, 1.0)
    apex_score = clip(1.0 - (days_to_apex / max(cfg.max_days_to_apex, 1)), 0.0, 1.0)
    touch_score = clip((high_touches + low_touches) / (cfg.min_touches * 2 + 4), 0.0, 1.0)
    volume_score = 1.0 if volume_contracting else 0.4

    score = (
        squeeze_score * 30
        + quality_score * 25
        + apex_score * 20
        + touch_score * 15
        + volume_score * 10
    )

    return {
        "score": round(float(score), 2),
        "close": round(last_close, 2),
        "upper_slope": round(m_high, 6),
        "lower_slope": round(m_low, 6),
        "upper_r2": round(r2_high, 4),
        "lower_r2": round(r2_low, 4),
        "start_width": round(start_width, 2),
        "end_width": round(end_width, 2),
        "end_width_ratio": round(end_width_ratio, 4),
        "days_to_apex": round(days_to_apex, 2),
        "touch_highs": high_touches,
        "touch_lows": low_touches,
        "avg_volume_20d": round(avg_volume_20d, 2),
        "volume_contracting": volume_contracting,
        "last_date": pd.to_datetime(recent["날짜"].iloc[-1]).strftime("%Y-%m-%d"),
        "recent": recent,
        "high_idx": high_idx,
        "low_idx": low_idx,
        "m_high": m_high,
        "b_high": b_high,
        "m_low": m_low,
        "b_low": b_low,
    }


# ---------- charting ----------

def save_chart(result: ScanResult, recent: pd.DataFrame, high_idx: np.ndarray, low_idx: np.ndarray,
               m_high: float, b_high: float, m_low: float, b_low: float, output_dir: str) -> str:
    chart_dir = os.path.join(output_dir, "charts")
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, f"{result.ticker}_{result.name}.png")

    x = recent["x"].to_numpy()
    close = recent["종가"].to_numpy()

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.plot(recent["날짜"], close, label="Close", linewidth=1.4)
    ax.plot(recent["날짜"], m_high * x + b_high, label="Upper trendline", linestyle="--")
    ax.plot(recent["날짜"], m_low * x + b_low, label="Lower trendline", linestyle="--")
    ax.scatter(recent.loc[high_idx, "날짜"], recent.loc[high_idx, "고가"], s=28, label="Swing highs")
    ax.scatter(recent.loc[low_idx, "날짜"], recent.loc[low_idx, "저가"], s=28, label="Swing lows")
    ax.set_title(f"{result.name} ({result.ticker}) | score={result.score}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(chart_path, dpi=140)
    plt.close(fig)
    return chart_path


# ---------- main scanner ----------

def scan_market(cfg: ScanConfig) -> pd.DataFrame:
    ensure_output_dir(cfg.output_dir)

    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=cfg.history_days * 2)).strftime("%Y%m%d")

    rows: list[dict] = []
    tickers = get_tickers(cfg.market)
    if cfg.max_tickers:
        tickers = tickers[: cfg.max_tickers]

    print(f"[INFO] market={cfg.market} ticker_count={len(tickers)}")

    for i, ticker in enumerate(tickers, start=1):
        try:
            name = stock.get_market_ticker_name(ticker)
            if not is_common_stock_name(name):
                continue

            df = stock.get_market_ohlcv(start_date, end_date, ticker)
            if df is None or df.empty:
                continue

            df = df.tail(cfg.history_days).copy()
            if len(df) < max(cfg.lookback_days, 80):
                continue

            analysis = analyze_triangle(df, cfg)
            if not analysis:
                continue

            result = ScanResult(
                ticker=ticker,
                name=name,
                score=analysis["score"],
                close=analysis["close"],
                upper_slope=analysis["upper_slope"],
                lower_slope=analysis["lower_slope"],
                upper_r2=analysis["upper_r2"],
                lower_r2=analysis["lower_r2"],
                start_width=analysis["start_width"],
                end_width=analysis["end_width"],
                end_width_ratio=analysis["end_width_ratio"],
                days_to_apex=analysis["days_to_apex"],
                touch_highs=analysis["touch_highs"],
                touch_lows=analysis["touch_lows"],
                avg_volume_20d=analysis["avg_volume_20d"],
                volume_contracting=analysis["volume_contracting"],
                last_date=analysis["last_date"],
            )

            if cfg.charts:
                result.chart_path = save_chart(
                    result=result,
                    recent=analysis["recent"],
                    high_idx=analysis["high_idx"],
                    low_idx=analysis["low_idx"],
                    m_high=analysis["m_high"],
                    b_high=analysis["b_high"],
                    m_low=analysis["m_low"],
                    b_low=analysis["b_low"],
                    output_dir=cfg.output_dir,
                )

            rows.append(asdict(result))
            print(f"[HIT] {name}({ticker}) score={result.score}")
        except KeyboardInterrupt:  # pragma: no cover
            raise
        except Exception as e:
            print(f"[WARN] {ticker} skipped: {e}")

    if not rows:
        return pd.DataFrame(columns=[field.name for field in ScanResult.__dataclass_fields__.values()])

    out = pd.DataFrame(rows).sort_values(
        by=["score", "touch_highs", "touch_lows", "upper_r2", "lower_r2"],
        ascending=[False, False, False, False, False],
    )
    out = out.head(cfg.top_n).reset_index(drop=True)

    csv_path = os.path.join(cfg.output_dir, f"triangle_scan_{cfg.market.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    out.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"[DONE] saved report -> {csv_path}")
    return out


# ---------- CLI ----------

def parse_args() -> ScanConfig:
    p = argparse.ArgumentParser(description="KRX 삼각수렴 차트 스캐너")
    p.add_argument("--market", default="KOSPI", choices=["KOSPI", "KOSDAQ", "KONEX", "ALL"], help="스캔 시장")
    p.add_argument("--lookback-days", type=int, default=90, help="패턴을 찾을 최근 거래일 수")
    p.add_argument("--history-days", type=int, default=180, help="일봉 로드 기간")
    p.add_argument("--swing-window", type=int, default=5, help="스윙 고점/저점 최소 간격")
    p.add_argument("--min-touches", type=int, default=3, help="상하단 최소 접촉 횟수")
    p.add_argument("--min-avg-volume", type=int, default=150000, help="20일 평균 거래량 하한")
    p.add_argument("--min-price", type=int, default=2000, help="주가 하한")
    p.add_argument("--max-price", type=int, default=None, help="주가 상한")
    p.add_argument("--max-tickers", type=int, default=None, help="앞에서부터 검사할 종목 수 제한")
    p.add_argument("--top-n", type=int, default=20, help="상위 결과 개수")
    p.add_argument("--charts", action="store_true", help="후보 차트 PNG 저장")
    p.add_argument("--output-dir", default="triangle_reports", help="리포트 저장 경로")
    p.add_argument("--prominence-ratio", type=float, default=0.018, help="스윙 검출 prominence 비율")
    p.add_argument("--min-r2", type=float, default=0.45, help="추세선 최소 적합도")
    p.add_argument("--max-days-to-apex", type=int, default=25, help="현재 시점에서 apex 까지 최대 일수")
    p.add_argument("--max-end-width-ratio", type=float, default=0.65, help="끝 폭/시작 폭 최대 비율")
    p.add_argument("--price-tolerance-ratio", type=float, default=0.02, help="추세선 오차 허용 비율")
    p.add_argument("--volume-contract-ratio", type=float, default=0.95, help="후반 거래량 수축 기준")

    ns = p.parse_args()
    return ScanConfig(
        market=ns.market,
        lookback_days=ns.lookback_days,
        history_days=ns.history_days,
        swing_window=ns.swing_window,
        min_touches=ns.min_touches,
        min_avg_volume=ns.min_avg_volume,
        min_price=ns.min_price,
        max_price=ns.max_price,
        max_tickers=ns.max_tickers,
        charts=ns.charts,
        top_n=ns.top_n,
        output_dir=ns.output_dir,
        prominence_ratio=ns.prominence_ratio,
        min_r2=ns.min_r2,
        max_days_to_apex=ns.max_days_to_apex,
        max_end_width_ratio=ns.max_end_width_ratio,
        price_tolerance_ratio=ns.price_tolerance_ratio,
        volume_contract_ratio=ns.volume_contract_ratio,
    )


def main() -> None:
    cfg = parse_args()
    print("[CONFIG]", cfg)
    scan_market(cfg)


if __name__ == "__main__":
    main()
