#!/usr/bin/env python3
"""Generate a daily triangle-pattern report for KRX stocks.

This script is designed for local cron/GitHub Actions usage.
It scans the market, writes latest CSV/JSON, and creates a markdown summary.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from triangle_scanner_webapp.triangle_scanner_krx import ScanConfig, scan_market


KST = ZoneInfo("Asia/Seoul")
UTC = ZoneInfo("UTC")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Daily KRX triangle report generator")
    p.add_argument("--market", default="ALL", choices=["KOSPI", "KOSDAQ", "KONEX", "ALL"])
    p.add_argument("--top-n", type=int, default=30, help="How many candidates to keep")
    p.add_argument("--max-tickers", type=int, default=900, help="Ticker scan cap")
    p.add_argument("--lookback-days", type=int, default=90)
    p.add_argument("--history-days", type=int, default=180)
    p.add_argument("--output-dir", default="triangle_scanner_webapp/reports")
    return p.parse_args()


def build_config(ns: argparse.Namespace) -> ScanConfig:
    return ScanConfig(
        market=ns.market,
        lookback_days=ns.lookback_days,
        history_days=ns.history_days,
        max_tickers=ns.max_tickers,
        top_n=ns.top_n,
        charts=False,
        output_dir=ns.output_dir,
    )


def write_markdown(df: pd.DataFrame, output_path: Path, now_utc: datetime) -> None:
    now_kst = now_utc.astimezone(KST)

    lines: list[str] = []
    lines.append("# KRX 삼각수렴 데일리 리포트")
    lines.append("")
    lines.append(f"- 생성 시각 (KST): **{now_kst.strftime('%Y-%m-%d %H:%M:%S')}**")
    lines.append(f"- 생성 시각 (UTC): **{now_utc.strftime('%Y-%m-%d %H:%M:%S')}**")
    lines.append(f"- 후보 종목 수: **{len(df)}개**")
    lines.append("")

    if df.empty:
        lines.append("> 오늘 조건에 맞는 삼각수렴 후보를 찾지 못했습니다.")
    else:
        display = df.copy()
        bool_cols = [c for c in ["volume_contracting"] if c in display.columns]
        for c in bool_cols:
            display[c] = display[c].map({True: "Y", False: "N"})

        wanted_cols = [
            "ticker",
            "name",
            "score",
            "close",
            "days_to_apex",
            "touch_highs",
            "touch_lows",
            "upper_r2",
            "lower_r2",
            "end_width_ratio",
            "volume_contracting",
            "last_date",
        ]
        cols = [c for c in wanted_cols if c in display.columns]

        lines.append("## 상위 후보")
        lines.append("")
        lines.append(display[cols].to_markdown(index=False))
        lines.append("")
        lines.append("## 참고")
        lines.append("- 본 결과는 자동 매매 신호가 아닌 **후보 스크리닝**입니다.")
        lines.append("- 실제 매매 전 뉴스/수급/재무/장세를 반드시 추가 검토하세요.")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ns = parse_args()
    cfg = build_config(ns)

    report_dir = Path(cfg.output_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    now_utc = datetime.now(tz=UTC)
    stamp = now_utc.strftime("%Y%m%d_%H%M%S")

    print("[INFO] start daily scan")
    scan_error = None
    try:
        df = scan_market(cfg)
    except Exception as exc:
        scan_error = str(exc)
        print(f"[WARN] scan failed: {scan_error}")
        df = pd.DataFrame()

    latest_csv = report_dir / "latest_candidates.csv"
    dated_csv = report_dir / f"candidates_{stamp}.csv"
    df.to_csv(latest_csv, index=False, encoding="utf-8-sig")
    df.to_csv(dated_csv, index=False, encoding="utf-8-sig")

    latest_json = report_dir / "latest_candidates.json"
    latest_json.write_text(df.to_json(orient="records", force_ascii=False, indent=2), encoding="utf-8")

    metadata = {
        "generated_at_utc": now_utc.strftime("%Y-%m-%d %H:%M:%S"),
        "generated_at_kst": now_utc.astimezone(KST).strftime("%Y-%m-%d %H:%M:%S"),
        "market": cfg.market,
        "top_n": cfg.top_n,
        "max_tickers": cfg.max_tickers,
        "count": int(len(df)),
        "scan_error": scan_error,
    }
    (report_dir / "latest_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    write_markdown(df, report_dir / "latest_report.md", now_utc)

    print(f"[DONE] rows={len(df)}")
    print(f"[DONE] report_dir={report_dir.resolve()}")


if __name__ == "__main__":
    main()
