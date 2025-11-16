以下は GitHub にそのまま貼れる完成度の README です。
アプリの概要、使い方、ロジックまで整理してあります。

📈 ペアトレード簡易Webアプリ

Pairs Trading Analysis App (Correlation / Cointegration / Hedge Ratio / Bollinger Band)

本アプリは、2つの株式銘柄を入力するだけで以下の分析を行える ペアトレード専用のWebアプリです。

Streamlit を利用しており、ローカル / Streamlit Cloud でそのまま動作します。

🚀 機能一覧
✔ 相関係数の計算

2銘柄の価格系列から Pearson 相関係数を算出。

✔ 共和分検定（Engle–Granger / ADF Test）

スプレッドの単位根を検定し、p < 0.05 で共和分あり と判定。

✔ ヘッジ比の推定（OLS β）

OLS 回帰を用いて price1 = α + β×price2 を推定。

✔ 株数ベースのヘッジ比算出

β を株価比で調整し、
「A株 1株に対し B株を何株？」
を自動算出。

✔ スプレッド・ボリンジャーバンド可視化

スプレッドとその ±2σ バンド を Plotly で描画。

✔ Zスコア（20日）

スプレッドの標準化値を計算し、売買シグナルの基礎に。

✔ シンプルな売買シグナル

Z > 2 → Aをショート / Bをロング

Z < -2 → Aをロング / Bをショート

|Z| < 0.5 → ポジションクローズ

📦 インストール
1. リポジトリを取得
git clone https://github.com/xxxx/pairs-trading-app.git
cd pairs-trading-app

2. 必要パッケージのインストール
pip install -r requirements.txt

▶️ 実行方法
streamlit run app.py


ブラウザが自動で開き、アプリが起動します。

🧠 アプリのロジック
1. データ取得

Yahoo Finance API（yfinance）で 2 年間の株価データを取得。

data = yf.download([t1, t2], period="2y")["Close"].dropna()

2. 相関係数
corr = price1.corr(price2)

3. 共和分検定（Engle–Granger）

OLS → スプレッド → ADF Test の順で実施。

X = sm.add_constant(price2)
model = sm.OLS(price1, X).fit()
spread = price1 - (alpha + beta * price2)
pvalue = adfuller(spread)[1]

4. ヘッジ比（β）
alpha, beta = model.params

5. 株数換算したヘッジ比
hedge_ratio = β × (price2_now / price1_now)


例：
「A株1株に対して B株を何株？」を算出。

6. ボリンジャーバンド
ma = spread.rolling(20).mean()
std = spread.rolling(20).std()
upper = ma + 2*std
lower = ma - 2*std

7. Zスコア
Z = (spread - MA20) / STD20

📊 使用技術

Python 3.10+

Streamlit

yfinance

pandas / numpy

statsmodels

plotly

📁 ファイル構成例
/
├── app.py              # Streamlitアプリ本体
├── requirements.txt    # 必要パッケージ
└── README.md
