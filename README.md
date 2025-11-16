📈 ペアトレード簡易Webアプリ  
**Pairs Trading Analysis App (Correlation / Cointegration / Hedge Ratio / Bollinger Band)**

本アプリは、2つの株式銘柄を入力するだけで以下の分析を行える **ペアトレード専用のWebアプリ**です。

Streamlit を利用しており、ローカル / Streamlit Cloud でそのまま動作します。

# 📘 ペアトレードとは？
ペアトレード（Pairs Trading）とは、**統計的裁定取引（Statistical Arbitrage）の一種**であり、  
2つの銘柄の「価格関係（スプレッド）」が**一定の範囲に収束する性質**を利用して利益を狙う投資手法です。

### 🔑 主要ポイント
- 2銘柄は「共に動きやすい」関係（相関 or 共和分）にある  
- 価格差（スプレッド）が平均から乖離すると **やがて平均回帰する** と期待  
- 割高な銘柄をショート、割安な銘柄をロング  
- 市場全体の上げ下げに影響されにくい（マーケットニュートラル）

### 例：三菱商事（8058.T） vs 伊藤忠（8001.T）
- 歴史的に動きが近い  
- 一時的に価格差が異常に広がれば  
  → 割高側をショート  
  → 割安側をロング  
- 価格差が元に戻れば利益確定

本アプリは、この「平均回帰」を数学的に判断するための  
**相関・共和分検定・Zスコア・ヘッジ比・BB** を自動で可視化します。

---

## 🚀 機能一覧

### ✔ 相関係数の計算  
2銘柄の価格系列から Pearson 相関係数を算出。

### ✔ 共和分検定（Engle–Granger / ADF Test）  
スプレッドの単位根を検定し、**p < 0.05 で共和分あり** と判定。

### ✔ ヘッジ比の推定（OLS β）  
OLS 回帰を用いて **price1 = α + β×price2** を推定。

### ✔ 株数ベースのヘッジ比算出  
β を株価比で調整し、  
**「A株 1株に対し B株を何株？」**  
を自動算出。

### ✔ スプレッド・ボリンジャーバンド可視化  
スプレッドとその **±2σ バンド** を Plotly で描画。
<img width="1140" height="550" alt="image" src="https://github.com/user-attachments/assets/34aa23a3-0f37-440d-8141-3cc6d228aac0" />


そのペアの動きを可視化できるので、研究・投資判断に利用してください。

### ✔ Zスコア（20日）  
スプレッドの標準化値を計算し、売買シグナルの基礎に。

### ✔ シンプルな売買シグナル  
- Z > 2 → Aをショート / Bをロング  
- Z < -2 → Aをロング / Bをショート  
- |Z| < 0.5 → ポジションクローズ  


---

## 📦 インストール

### 1. リポジトリを取得

```
git clone https://github.com/xxxx/pairs-trading-app.git
cd pairs-trading-app
```

### 2. 必要パッケージのインストール

```
pip install -r requirements.txt
```

---

## ▶️ 実行方法

```
streamlit run app.py
```

ブラウザが自動で開き、アプリが起動します。

---

## 🧠 アプリのロジック

### 1. データ取得

Yahoo Finance API（yfinance）で 2 年間の株価データを取得。

```python
data = yf.download([t1, t2], period="2y")["Close"].dropna()
```

### 2. 相関係数

```python
corr = price1.corr(price2)
```

### 3. 共和分検定（Engle–Granger）

OLS → スプレッド → ADF Test の順で実施。

```python
X = sm.add_constant(price2)
model = sm.OLS(price1, X).fit()
spread = price1 - (alpha + beta * price2)
pvalue = adfuller(spread)[1]
```

### 4. ヘッジ比（β）

```python
alpha, beta = model.params
```

### 5. 株数換算したヘッジ比

```
hedge_ratio = β × (price2_now / price1_now)
```

例：  
「A株1株に対して B株を何株？」を算出。

### 6. ボリンジャーバンド

```python
ma = spread.rolling(20).mean()
std = spread.rolling(20).std()
upper = ma + 2*std
lower = ma - 2*std
```

### 7. Zスコア

```
Z = (spread - MA20) / STD20
```

---

## 📊 使用技術

- **Python 3.10+**
- **Streamlit**
- **yfinance**
- **pandas / numpy**
- **statsmodels**
- **plotly**

---

## 📁 ファイル構成例

```
/
├── app.py              # Streamlitアプリ本体
├── requirements.txt    # 必要パッケージ
└── README.md
```

---

## 📝 ライセンス
MIT License
