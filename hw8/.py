import numpy as np
import matplotlib.pyplot as plt
import random
import math
import copy

# 設定隨機種子以確保每次生成的城市座標與初始路徑相同
np.random.seed(42)
random.seed(42)

NUM_CITIES = 20
CITIES = np.random.rand(NUM_CITIES, 2) * 100

def calc_distance(city1, city2):
    return np.linalg.norm(city1 - city2)

# 建立距離矩陣
DIST_MATRIX = np.zeros((NUM_CITIES, NUM_CITIES))
for i in range(NUM_CITIES):
    for j in range(NUM_CITIES):
        DIST_MATRIX[i][j] = calc_distance(CITIES[i], CITIES[j])

def tour_length(tour):
    return sum(DIST_MATRIX[tour[i]][tour[(i + 1) % NUM_CITIES]] for i in range(NUM_CITIES))

# 共同的隨機初始路徑
INITIAL_TOUR = list(range(NUM_CITIES))
random.shuffle(INITIAL_TOUR)

# ==========================================
# 1. 改良法 (Improvement Method - 2-Opt)
# ==========================================
def two_opt(tour):
    best_tour = copy.deepcopy(tour)
    best_dist = tour_length(best_tour)
    improved = True
    while improved:
        improved = False
        for i in range(1, NUM_CITIES - 1):
            for j in range(i + 1, NUM_CITIES):
                if j - i == 1: continue # 相鄰節點反轉無意義
                new_tour = best_tour[:]
                new_tour[i:j] = best_tour[j-1:i-1:-1] # 2-opt 反轉片段
                new_dist = tour_length(new_tour)
                if new_dist < best_dist:
                    best_dist = new_dist
                    best_tour = new_tour
                    improved = True
        if improved:
            break # 為了簡化，找到一次完整改良循環即結束（或可設為跑到局部最佳）
    return best_tour, best_dist

# ==========================================
# 2. 爬山演算法 (Hill Climbing - First Choice)
# ==========================================
def hill_climbing(tour, max_iter=1000):
    current_tour = copy.deepcopy(tour)
    current_dist = tour_length(current_tour)
    
    for _ in range(max_iter):
        # 隨機生成一個鄰居 (交換兩個城市)
        i, j = random.sample(range(NUM_CITIES), 2)
        new_tour = current_tour[:]
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        new_dist = tour_length(new_tour)
        
        # 只要更好就移動 (First Choice)
        if new_dist < current_dist:
            current_tour = new_tour
            current_dist = new_dist
            
    return current_tour, current_dist

# ==========================================
# 3. 模擬退火法 (Simulated Annealing)
# ==========================================
def simulated_annealing(tour, initial_temp=1000, cooling_rate=0.995, min_temp=1):
    current_tour = copy.deepcopy(tour)
    current_dist = tour_length(current_tour)
    best_tour = copy.deepcopy(current_tour)
    best_dist = current_dist
    
    temp = initial_temp
    while temp > min_temp:
        i, j = random.sample(range(NUM_CITIES), 2)
        new_tour = current_tour[:]
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        new_dist = tour_length(new_tour)
        
        # 判斷是否接受新解
        if new_dist < current_dist or random.random() < math.exp((current_dist - new_dist) / temp):
            current_tour = new_tour
            current_dist = new_dist
            if current_dist < best_dist:
                best_dist = current_dist
                best_tour = copy.deepcopy(current_tour)
                
        temp *= cooling_rate
        
    return best_tour, best_dist

# ==========================================
# 4. 梯度下降法 (Discrete Steepest Descent)
# ==========================================
def discrete_gradient_descent(tour):
    current_tour = copy.deepcopy(tour)
    current_dist = tour_length(current_tour)
    
    while True:
        best_neighbor_tour = None
        best_neighbor_dist = current_dist
        
        # 評估「所有」鄰居，找出下降最快的方向 (Steepest edge)
        for i in range(NUM_CITIES):
            for j in range(i + 1, NUM_CITIES):
                new_tour = current_tour[:]
                new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
                new_dist = tour_length(new_tour)
                
                if new_dist < best_neighbor_dist:
                    best_neighbor_dist = new_dist
                    best_neighbor_tour = new_tour
                    
        # 如果無法再下降（梯度為0），則停止
        if best_neighbor_tour is None:
            break
        else:
            current_tour = best_neighbor_tour
            current_dist = best_neighbor_dist
            
    return current_tour, current_dist

# ==========================================
# 5. 貪婪演算法 (Greedy / Nearest Neighbor)
# ==========================================
def greedy_algorithm():
    unvisited = list(range(NUM_CITIES))
    current_city = random.choice(unvisited)
    tour = [current_city]
    unvisited.remove(current_city)
    
    while unvisited:
        nearest_city = min(unvisited, key=lambda city: DIST_MATRIX[current_city][city])
        tour.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city
        
    return tour, tour_length(tour)

# ==========================================
# 執行與繪圖
# ==========================================
def plot_tour(ax, tour, distance, title):
    tour_coords = CITIES[tour + [tour[0]]] # 閉環
    ax.plot(tour_coords[:, 0], tour_coords[:, 1], marker='o', linestyle='-', color='b', markersize=5)
    ax.plot(tour_coords[0, 0], tour_coords[0, 1], marker='s', color='r', markersize=8) # 起點
    ax.set_title(f"{title}\nDist: {distance:.2f}")
    ax.set_xticks([])
    ax.set_yticks([])

results = {
    "Improvement (2-Opt)": two_opt(INITIAL_TOUR),
    "Hill Climbing": hill_climbing(INITIAL_TOUR),
    "Simulated Annealing": simulated_annealing(INITIAL_TOUR),
    "Gradient Descent (Steepest)": discrete_gradient_descent(INITIAL_TOUR),
    "Greedy (Nearest)": greedy_algorithm()
}

fig, axes = plt.subplots(1, 5, figsize=(22, 4))
fig.suptitle("Traveling Salesperson Problem (TSP) - 5 Algorithms Comparison", fontsize=16)

for ax, (title, (tour, dist)) in zip(axes, results.items()):
    plot_tour(ax, tour, dist, title)

plt.tight_layout()
plt.show()
