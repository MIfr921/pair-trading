import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import plotly.graph_objects as go


st.title("📈 ペアトレード簡易Webアプリ（相関・共和分・BB・ヘッジ比）")

# ======================
#  入 力
# ======================
col1, col2 = st.columns(2)
t1 = col1.text_input("銘柄1（例：8058.T）", "8058.T")
t2 = col2.text_input("銘柄2（例：8001.T）", "8001.T")

if st.button("分析開始"):
    # -----------------------
    #  データ取得
    # -----------------------
    data = yf.download([t1, t2], period="2y")["Close"].dropna()
    price1 = data[t1]
    price2 = data[t2]

    st.subheader("① 相関係数")
    corr = price1.corr(price2)
    st.write(f"**相関係数 = {corr:.3f}**")

    # -----------------------
    #  OLS回帰 → スプレッド
    # -----------------------
    X = sm.add_constant(price2)
    model = sm.OLS(price1, X).fit()
    alpha, beta = model.params

    spread = price1 - (alpha + beta * price2)

    st.subheader("② 共和分検定（Engle–Granger ADF Test）")
    adf_p = adfuller(spread.dropna())[1]
    st.write(f"ADF p-value = **{adf_p:.4f}**")
    if adf_p < 0.05:
        st.success("📌 共和分あり（ペアトレード有効の可能性）")
    else:
        st.warning("共和分なし（スプレッドが安定していない可能性）")

    # -----------------------
    #  ヘッジ比（株数換算）
    # -----------------------
    st.subheader("③ ヘッジ比（OLS β）と株数換算")
    price1_now = price1.iloc[-1]
    price2_now = price2.iloc[-1]

    hedge_ratio = beta * (price2_now / price1_now)

    st.write(f"OLS β = **{beta:.3f}**")
    st.write(f"{t1} 1株に対して {t2} を **{hedge_ratio:.2f} 株** 取るとヘッジバランス")

    # -----------------------
    #  ボリンジャーバンド
    # -----------------------
    st.subheader("④ スプレッドのボリンジャーバンド")

    ma = spread.rolling(20).mean()
    std = spread.rolling(20).std()
    upper = ma + 2*std
    lower = ma - 2*std

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=spread.index, y=spread, mode='lines', name='Spread'))
    fig.add_trace(go.Scatter(x=ma.index, y=ma, mode='lines', name='MA(20)'))
    fig.add_trace(go.Scatter(x=upper.index, y=upper, mode='lines', name='Upper Band'))
    fig.add_trace(go.Scatter(x=lower.index, y=lower, mode='lines', name='Lower Band'))

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------
    #  Zスコア
    # -----------------------
    st.subheader("⑤ Zスコア")
    z = (spread - ma) / std
    st.line_chart(z)

    latest_z = z.dropna().iloc[-1]
    st.write(f"最新Zスコア = **{latest_z:.2f}**")

    # -----------------------
    # シグナル例
    # -----------------------
    st.subheader("⑥ シンプル取引シグナル")
    if latest_z > 2:
        st.error(f"Z>2 → **{t1} をショート、{t2} をロング**")
    elif latest_z < -2:
        st.error(f"Z<-2 → **{t1} をロング、{t2} をショート**")
    else:
        st.info("レンジ内 → No Trade")
