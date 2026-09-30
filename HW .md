# 經典迭代演算法統一框架

使用 Python 與 NumPy 實作多種經典迭代演算法，並透過一個通用的 `generic_iterator()` 框架統一管理「狀態更新」與「收斂判斷」。

---

## 📌 專案介紹

許多數值分析、線性代數與機器學習演算法，都具有類似的流程：

```text
設定初始值
    ↓
計算下一個狀態
    ↓
判斷是否收斂
    ↓
未收斂 → 繼續迭代
    ↓
收斂 → 輸出結果
```

本專案將這個共同流程抽象成：

```python
generic_iterator()
```

再將不同演算法的「狀態更新方式」與「收斂條件」傳入，讓不同的演算法可以共用同一套迭代框架。

---

## 🎯 專案目的

本專案主要有以下目的：

* 理解迭代法的基本概念
* 學習如何設計通用的程式框架
* 使用 NumPy 進行向量與矩陣運算
* 比較不同經典演算法的迭代方式
* 了解「狀態更新」與「收斂判斷」的概念
* 將數值分析與機器學習演算法統一到相同的程式架構

---

## 🧰 使用工具

* Python 3
* NumPy

安裝 NumPy：

```bash
pip install numpy
```

---

## 📂 專案內容

本程式包含以下 9 種演算法：

| 編號 | 演算法                   | 主要用途          |
| -- | --------------------- | ------------- |
| 1  | Fixed-Point Iteration | 求不動點          |
| 2  | Newton's Method       | 求方程式的根        |
| 3  | Gauss-Seidel          | 求解線性方程組       |
| 4  | Power Iteration       | 求最大特徵值與特徵向量   |
| 5  | QR Algorithm          | 求矩陣特徵值        |
| 6  | RK4                   | 求解常微分方程式      |
| 7  | PageRank              | 計算網頁重要程度      |
| 8  | K-Means               | 資料分群          |
| 9  | EM Algorithm          | 估計含有潛在變數的模型參數 |

---

# 1. 通用迭代框架

整個專案最核心的函式是：

```python
def generic_iterator(
    transition_func,
    is_converged,
    initial_state,
    max_iter=1000
):
```

它將迭代演算法分成三個部分：

### 初始狀態

```python
initial_state
```

代表演算法開始時的資料。

例如：

```python
initial_state=1.0
```

或：

```python
initial_state=np.zeros(n)
```

---

### 狀態更新函式

```python
transition_func
```

負責將目前狀態轉換成下一個狀態。

概念為：

$$
x_{k+1}=g(x_k)
$$

例如：

```python
transition = lambda x: x - f(x) / df(x)
```

---

### 收斂判斷

```python
is_converged
```

判斷目前結果是否已經足夠接近答案。

例如：

```python
converged = lambda old, new, i: abs(new - old) < 1e-6
```

代表新舊結果差距小於：

$$
10^{-6}
$$

時停止迭代。

---

# 2. Fixed-Point Iteration

## 二維不動點迭代法

不動點迭代的基本形式：

$$
x_{k+1}=g(x_k)
$$

如果最後：

$$
x_{k+1}\approx x_k
$$

就表示結果已經接近不動點。

本程式使用二維向量：

```python
X = [x, y]
```

並透過：

```python
np.linalg.norm(new - old)
```

計算新舊向量之間的距離。

### 用途

* 求非線性方程式的不動點
* 數值分析
* 迭代式計算

---

# 3. Newton's Method

## 牛頓法求根

本程式使用：

$$
f(x)=x^2-4
$$

因此實際上是在求：

$$
x^2-4=0
$$

答案為：

$$
x=2
$$

或：

$$
x=-2
$$

牛頓法公式：

$$
x_{k+1}
=
x_k-\frac{f(x_k)}{f'(x_k)}
$$

程式：

```python
f = lambda x: x**2 - 4.0
df = lambda x: 2.0 * x

transition = lambda x: x - f(x) / df(x)
```

初始值：

```python
initial_state=1.0
```

因此會逐漸接近：

```text
2
```

---

# 4. Gauss-Seidel

## 高斯－賽得爾法

Gauss-Seidel 用來求解線性方程組：

$$
Ax=b
$$

本程式使用：

```python
A = np.array([
    [4.0, -1.0, 0.0],
    [-1.0, 4.0, -1.0],
    [0.0, -1.0, 4.0]
])
```

以及：

```python
b = np.array([7.0, 2.0, 13.0])
```

每次利用最新計算出的變數更新下一個變數。

收斂條件：

```python
np.max(np.abs(new - old)) < 1e-6
```

### 用途

* 解線性方程組
* 數值分析
* 科學計算

---

# 5. Power Iteration

## 冪次迭代法

Power Iteration 主要用來尋找矩陣的最大特徵值以及對應的特徵向量。

基本概念：

$$
v_{k+1}=\frac{Av_k}{\|Av_k\|}
$$

程式：

```python
transition = lambda v: np.dot(A, v) / np.linalg.norm(np.dot(A, v))
```

每次將矩陣與目前向量相乘，再進行正規化。

最後使用：

```python
eigenval = np.dot(v_result, np.dot(A, v_result))
```

估計最大特徵值。

### 用途

* 特徵值計算
* 主成分分析相關概念
* PageRank
* 矩陣分析

---

# 6. QR Algorithm

## QR 演算法

QR Algorithm 可以用來計算矩陣的特徵值。

首先將矩陣分解：

$$
A_k=Q_kR_k
$$

接著計算：

$$
A_{k+1}=R_kQ_k
$$

重複進行：

```text
A
↓
QR 分解
↓
R × Q
↓
新的 A
↓
繼續迭代
```

當矩陣逐漸接近對角矩陣時：

```text
[a 0 0]
[0 b 0]
[0 0 c]
```

對角線上的數值就可以作為特徵值的近似值。

---

# 7. RK4

## 龍格－庫塔四階法

RK4（Runge-Kutta 4th Order Method）用來近似求解常微分方程式。

本程式使用：

$$
\frac{dy}{dt}=y-t+1
$$

RK4 每一步會計算：

$$
k_1
$$

$$
k_2
$$

$$
k_3
$$

$$
k_4
$$

最後：

$$
y_{n+1}
=
y_n+
\frac{h}{6}
(k_1+2k_2+2k_3+k_4)
$$

程式中：

```python
k1 = f(t, y)

k2 = f(
    t + 0.5 * h,
    y + 0.5 * h * k1
)

k3 = f(
    t + 0.5 * h,
    y + 0.5 * h * k2
)

k4 = f(
    t + h,
    y + h * k3
)
```

### 用途

* 常微分方程式
* 物理模擬
* 工程計算
* 數值分析

---

# 8. PageRank

## PageRank 網頁排名演算法

PageRank 是一種透過網頁之間的連結關係，計算網頁重要程度的方法。

本程式使用轉移矩陣：

```python
M
```

並加入阻尼係數：

```python
d = 0.85
```

建立 Google Matrix：

```python
G = d * M + (1 - d) / n * np.ones((n, n))
```

接著反覆計算：

```python
r_next = G @ r
```

直到結果收斂。

最後得到：

```text
網頁權重分佈
```

數值越大代表該網頁在此模型中具有較高的 PageRank 權重。

---

# 9. K-Means

## K-Means 聚類

K-Means 是常見的非監督式機器學習演算法。

本程式將資料分成：

```python
k = 2
```

個群組。

主要分成兩個步驟：

### E-Step

計算每個資料點與各個中心點的距離。

```python
distances = np.linalg.norm(
    X[:, np.newaxis] - centroids,
    axis=2
)
```

再將資料分配給距離最近的中心：

```python
labels = np.argmin(distances, axis=1)
```

### M-Step

重新計算每一群的平均值：

```python
return np.array([
    X[labels == j].mean(axis=0)
    for j in range(k)
])
```

然後得到新的中心點。

重複：

```text
分配資料
 ↓
更新中心
 ↓
分配資料
 ↓
更新中心
 ↓
直到收斂
```

---

# 10. EM Algorithm

## Two-Coin EM 演算法

本程式使用兩枚硬幣的例子展示 EM（Expectation-Maximization）演算法。

兩個參數：

```python
theta_A
theta_B
```

分別代表兩枚硬幣出現正面的機率。

初始值：

```python
init_theta = (0.6, 0.5)
```

EM 主要分成：

### E-Step

根據目前的參數，計算每組資料比較可能來自硬幣 A 或硬幣 B 的機率。

```python
p_A = l_A / (l_A + l_B)
p_B = 1.0 - p_A
```

### M-Step

利用 E-Step 計算出的機率重新估計參數：

```python
theta_A
theta_B
```

然後繼續迭代。

---

# 11. 統一框架的優點

傳統寫法可能需要在每個演算法中重複撰寫：

```python
for iteration in range(1000):
    ...
    
    if condition:
        break
```

本專案將這部分抽出來。

因此每個演算法只需要負責兩件事情：

### ① 如何計算下一個狀態

```python
transition
```

### ② 如何判斷是否收斂

```python
converged
```

例如牛頓法：

```python
transition = lambda x: x - f(x) / df(x)

converged = lambda old, new, i: abs(new - old) < 1e-6
```

最後交給：

```python
generic_iterator(
    transition,
    converged,
    initial_state=1.0
)
```

處理。

---

# 12. 程式執行流程

執行程式後，主程式會依序呼叫：

```python
demo_fixed_point()
demo_newton()
demo_gauss_seidel()
demo_power_iteration()
demo_qr_algorithm()
demo_rk4()
demo_pagerank()
demo_kmeans()
demo_em_two_coin()
```

因此會依序展示 9 種演算法的結果。

整體流程：

```text
開始
 │
 ↓
Fixed-Point
 │
 ↓
Newton
 │
 ↓
Gauss-Seidel
 │
 ↓
Power Iteration
 │
 ↓
QR Algorithm
 │
 ↓
RK4
 │
 ↓
PageRank
 │
 ↓
K-Means
 │
 ↓
EM
 │
 ↓
結束
```

---

# 13. 執行方式

將程式儲存為：

```text
iterative_algorithms.py
```

在終端機執行：

```bash
python iterative_algorithms.py
```

如果系統使用 `python3`：

```bash
python3 iterative_algorithms.py
```

---

# 14. 專案結構

推薦 GitHub 專案使用以下結構：

```text
iterative-algorithms/
│
├── README.md
│
├── iterative_algorithms.py
│
└── requirements.txt
```

`requirements.txt`：

```text
numpy
```

---

# 15. 範例輸出

程式執行後會看到類似：

```text
=========================================================
   全系列經典迭代演算法 - 統一抽象框架展示 (Unified Framework)
=========================================================

--- 1. 二維不動點迭代法 (Fixed-Point Iteration) ---
結果: [...]

--- 2. 牛頓法求根 (Newton's Method: x^2 - 4 = 0) ---
結果: 根 x = 2.000000

--- 3. 高斯-賽得爾法 (Gauss-Seidel Linear Solver) ---
結果: x = [...]

--- 4. 冪次迭代法 (Power Iteration: SVD / 主特徵向量) ---
結果: 最大特徵值 = [...]

--- 5. QR 演算法 (QR Algorithm: 計算所有特徵值) ---
結果: 所有特徵值 = [...]

--- 6. 龍格-庫塔法 (RK4 ODE Solver) ---
結果: ...

--- 7. PageRank ---
結果: 網頁權重分佈 = [...]

--- 8. K-Means 聚類 ---
結果: 最終分群中心 = ...

--- 9. EM 演算法 ---
結果: 估計硬幣機率 ...
```

實際數值會依照程式執行結果為準。

---

# 16. 核心概念總結

本專案最重要的概念不是單純實作 9 個演算法，而是了解這些演算法雖然用途不同，卻可以使用相同的迭代架構。

共同形式：

$$
State_{k+1}=Transition(State_k)
$$

並透過：

$$
Convergence(State_k,State_{k+1})
$$

判斷是否停止。

因此可以將不同演算法抽象成：

```text
                Generic Iterator
                       │
          ┌────────────┴────────────┐
          │                         │
    Transition Function       Convergence Test
          │                         │
          └────────────┬────────────┘
                       ↓
                    Iteration
                       ↓
                  Final Result
```

這種設計方式可以減少重複程式碼，也方便未來加入其他迭代演算法。

---

## 📚 使用到的主要技術

* Python
* NumPy
* Lambda Function
* Function Abstraction
* Iterative Algorithms
* Numerical Analysis
* Linear Algebra
* Machine Learning
* Matrix Computation

---

## 👨‍💻 作者

此專案用於學習與展示經典迭代演算法，以及通用迭代框架的設計概念。

