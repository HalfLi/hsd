from __future__ import annotations

from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from triangle_scanner_krx import (
    ScanConfig,
    analyze_triangle,
    get_tickers,
    is_common_stock_name,
    scan_market,
)
from pykrx import stock

st.set_page_config(page_title="KRX 삼각수렴 스캐너", layout="wide")


@st.cache_data(ttl=60 * 60)
def cached_tickers(market: str) -> list[str]:
    return get_tickers(market)


@st.cache_data(ttl=60 * 30, show_spinner=False)
def fetch_ohlcv(ticker: str, history_days: int) -> pd.DataFrame:
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=history_days * 2)).strftime("%Y%m%d")
    df = stock.get_market_ohlcv(start_date, end_date, ticker)
    if df is None or df.empty:
        return pd.DataFrame()
    return df.tail(history_days).copy()


def build_chart(ticker: str, name: str, df: pd.DataFrame, cfg: ScanConfig):
    analysis = analyze_triangle(df, cfg)
    if not analysis:
        return None

    recent = analysis["recent"]
    x = recent["x"].to_numpy()

    fig = plt.figure(figsize=(11, 5.5))
    ax = fig.add_subplot(111)
    ax.plot(recent["날짜"], recent["종가"], linewidth=1.6, label="Close")
    ax.plot(recent["날짜"], analysis["m_high"] * x + analysis["b_high"], linestyle="--", label="Upper trendline")
    ax.plot(recent["날짜"], analysis["m_low"] * x + analysis["b_low"], linestyle="--", label="Lower trendline")
    ax.scatter(recent.loc[analysis["high_idx"], "날짜"], recent.loc[analysis["high_idx"], "고가"], s=24, label="Swing highs")
    ax.scatter(recent.loc[analysis["low_idx"], "날짜"], recent.loc[analysis["low_idx"], "저가"], s=24, label="Swing lows")
    ax.set_title(f"{name} ({ticker}) | score={analysis['score']}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


@st.cache_data(ttl=60 * 30, show_spinner=False)
def run_scan_cached(
    market: str,
    lookback_days: int,
    history_days: int,
    swing_window: int,
    min_touches: int,
    min_avg_volume: int,
    min_price: int,
    max_price: Optional[int],
    top_n: int,
    max_tickers: Optional[int],
    prominence_ratio: float,
    min_r2: float,
    max_days_to_apex: int,
    max_end_width_ratio: float,
    price_tolerance_ratio: float,
    volume_contract_ratio: float,
) -> pd.DataFrame:
    cfg = ScanConfig(
        market=market,
        lookback_days=lookback_days,
        history_days=history_days,
        swing_window=swing_window,
        min_touches=min_touches,
        min_avg_volume=min_avg_volume,
        min_price=min_price,
        max_price=max_price,
        top_n=top_n,
        max_tickers=max_tickers,
        charts=False,
        output_dir="triangle_web_reports",
        prominence_ratio=prominence_ratio,
        min_r2=min_r2,
        max_days_to_apex=max_days_to_apex,
        max_end_width_ratio=max_end_width_ratio,
        price_tolerance_ratio=price_tolerance_ratio,
        volume_contract_ratio=volume_contract_ratio,
    )
    df = scan_market(cfg)
    if df.empty:
        return df
    keep_cols = [
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
        "avg_volume_20d",
        "volume_contracting",
        "last_date",
    ]
    return df[keep_cols].head(top_n).copy()


st.title("KRX 삼각수렴 스캐너")
st.caption("한국 주식에서 최근 수렴형 패턴 후보를 찾아주는 웹앱")

with st.sidebar:
    st.header("스캔 설정")
    market = st.selectbox("시장", ["KOSPI", "KOSDAQ", "ALL"], index=2)
    top_n = st.slider("상위 후보 개수", min_value=5, max_value=50, value=20, step=5)
    max_tickers = st.number_input("스캔 종목 수 제한 (0=전체)", min_value=0, max_value=4000, value=600, step=50)

    st.subheader("패턴 조건")
    lookback_days = st.slider("패턴 탐지 구간", 60, 140, 90, 5)
    history_days = st.slider("가져올 일봉 수", 120, 260, 180, 10)
    swing_window = st.slider("스윙 민감도", 3, 10, 5, 1)
    min_touches = st.slider("최소 접촉 횟수", 2, 5, 3, 1)
    min_avg_volume = st.number_input("20일 평균 거래량 하한", min_value=0, max_value=100000000, value=150000, step=50000)
    min_price = st.number_input("최소 주가", min_value=0, max_value=1000000, value=2000, step=500)
    max_price_raw = st.number_input("최대 주가 (0=제한 없음)", min_value=0, max_value=1000000, value=0, step=1000)
    max_price = None if max_price_raw == 0 else int(max_price_raw)

    st.subheader("정밀도")
    prominence_ratio = st.slider("스윙 강도 비율", 0.005, 0.050, 0.018, 0.001, format="%.3f")
    min_r2 = st.slider("추세선 적합도 최소치", 0.20, 0.90, 0.45, 0.01)
    max_days_to_apex = st.slider("Apex까지 최대 일수", 5, 40, 25, 1)
    max_end_width_ratio = st.slider("끝 폭 / 시작 폭 최대치", 0.20, 0.90, 0.65, 0.01)
    price_tolerance_ratio = st.slider("허용 오차 비율", 0.005, 0.050, 0.020, 0.001, format="%.3f")
    volume_contract_ratio = st.slider("거래량 수축 기준", 0.70, 1.10, 0.95, 0.01)

    run_btn = st.button("스캔 실행", use_container_width=True, type="primary")

c1, c2, c3 = st.columns(3)
with c1:
    try:
        total_tickers = len(cached_tickers(market))
    except Exception:
        total_tickers = None
    st.metric("시장 종목 수", total_tickers if total_tickers is not None else "-")
with c2:
    st.metric("이번 스캔 제한", "전체" if max_tickers == 0 else int(max_tickers))
with c3:
    st.metric("상위 표시 수", top_n)

st.markdown("---")

if "scan_df" not in st.session_state:
    st.session_state.scan_df = pd.DataFrame()
    st.session_state.last_cfg = None

if run_btn:
    with st.spinner("종목 스캔 중..."):
        df = run_scan_cached(
            market=market,
            lookback_days=lookback_days,
            history_days=history_days,
            swing_window=swing_window,
            min_touches=min_touches,
            min_avg_volume=int(min_avg_volume),
            min_price=int(min_price),
            max_price=max_price,
            top_n=top_n,
            max_tickers=None if max_tickers == 0 else int(max_tickers),
            prominence_ratio=prominence_ratio,
            min_r2=min_r2,
            max_days_to_apex=max_days_to_apex,
            max_end_width_ratio=max_end_width_ratio,
            price_tolerance_ratio=price_tolerance_ratio,
            volume_contract_ratio=volume_contract_ratio,
        )
    st.session_state.scan_df = df
    st.session_state.last_cfg = ScanConfig(
        market=market,
        lookback_days=lookback_days,
        history_days=history_days,
        swing_window=swing_window,
        min_touches=min_touches,
        min_avg_volume=int(min_avg_volume),
        min_price=int(min_price),
        max_price=max_price,
        top_n=top_n,
        max_tickers=None if max_tickers == 0 else int(max_tickers),
        charts=False,
        output_dir="triangle_web_reports",
        prominence_ratio=prominence_ratio,
        min_r2=min_r2,
        max_days_to_apex=max_days_to_apex,
        max_end_width_ratio=max_end_width_ratio,
        price_tolerance_ratio=price_tolerance_ratio,
        volume_contract_ratio=volume_contract_ratio,
    )

scan_df = st.session_state.scan_df
cfg = st.session_state.last_cfg

if scan_df.empty:
    st.info("왼쪽에서 조건을 잡고 '스캔 실행'을 누르세요.")
else:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.success(f"후보 {len(scan_df)}개를 찾았습니다.")
        st.dataframe(
            scan_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ticker": st.column_config.TextColumn("티커"),
                "name": st.column_config.TextColumn("종목명"),
                "score": st.column_config.NumberColumn("점수", format="%.2f"),
                "close": st.column_config.NumberColumn("현재가", format="%.2f"),
                "days_to_apex": st.column_config.NumberColumn("Apex까지 일수", format="%.2f"),
                "touch_highs": st.column_config.NumberColumn("상단 접촉"),
                "touch_lows": st.column_config.NumberColumn("하단 접촉"),
                "upper_r2": st.column_config.NumberColumn("상단 R²", format="%.3f"),
                "lower_r2": st.column_config.NumberColumn("하단 R²", format="%.3f"),
                "end_width_ratio": st.column_config.NumberColumn("끝 폭 비율", format="%.3f"),
                "avg_volume_20d": st.column_config.NumberColumn("20일 평균 거래량", format="%.0f"),
                "volume_contracting": st.column_config.CheckboxColumn("거래량 수축"),
                "last_date": st.column_config.TextColumn("기준일"),
            },
        )

        csv_data = scan_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "CSV 다운로드",
            data=csv_data,
            file_name=f"triangle_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

    with col2:
        ticker_options = [f"{row.name} ({row.ticker})" for row in scan_df.itertuples(index=False)]
        selected = st.selectbox("상세 차트 종목 선택", ticker_options)
        selected_row = scan_df.iloc[ticker_options.index(selected)]
        ticker = str(selected_row["ticker"])
        name = str(selected_row["name"])

        if cfg is not None:
            with st.spinner("차트 불러오는 중..."):
                raw_df = fetch_ohlcv(ticker, cfg.history_days)
                if raw_df.empty:
                    st.warning("일봉 데이터를 불러오지 못했습니다.")
                else:
                    fig = build_chart(ticker, name, raw_df, cfg)
                    if fig is None:
                        st.warning("현재 조건으로는 상세 차트를 그릴 수 없습니다.")
                    else:
                        st.pyplot(fig, use_container_width=True)
                        buf = BytesIO()
                        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
                        st.download_button(
                            "차트 PNG 다운로드",
                            data=buf.getvalue(),
                            file_name=f"{ticker}_{name}_triangle.png",
                            mime="image/png",
                        )

    st.markdown("---")
    st.caption("주의: 이 도구는 자동매매용이 아니라 후보 발굴용입니다. 최종 판단은 수동 검토가 필요합니다.")
