"""
Tower of Hanoi (河內塔問題)
包含兩種解法：
1. 遞迴解法 (Recursive Approach)
2. 非遞迴解法 (Iterative Approach - 使用 Stack 模擬遞迴)
"""

def hanoi_recursive(n, source, auxiliary, target):
    """
    遞迴版本的河內塔解法
    
    :param n: 圓盤數量
    :param source: 來源柱
    :param auxiliary: 輔助柱
    :param target: 目標柱
    """
    if n > 0:
        # 步驟 1：將上面的 n-1 個圓盤從 source 移到 auxiliary
        hanoi_recursive(n - 1, source, target, auxiliary)
        
        # 步驟 2：將最底層的第 n 個圓盤從 source 移到 target
        print(f"[遞迴] 移動圓盤 {n} : 從 {source} -> {target}")
        
        # 步驟 3：將 auxiliary 上的 n-1 個圓盤移到 target
        hanoi_recursive(n - 1, auxiliary, source, target)


def hanoi_iterative(n, source, auxiliary, target):
    """
    非遞迴（迭代）版本的河內塔解法
    利用 Stack (堆疊) 資料結構來模擬系統的 Call Stack
    
    :param n: 圓盤數量
    :param source: 來源柱
    :param auxiliary: 輔助柱
    :param target: 目標柱
    """
    # 堆疊中的每個元素為一個字典，儲存當前的狀態：
    # stage == 0 代表準備執行「移走上面 n-1 個圓盤」
    # stage == 1 代表準備執行「移動底部最大圓盤，並處理剩餘圓盤」
    stack = [{'n': n, 'src': source, 'aux': auxiliary, 'tgt': target, 'stage': 0}]
    
    while stack:
        frame = stack.pop()
        curr_n = frame['n']
        src = frame['src']
        aux = frame['aux']
        tgt = frame['tgt']
        stage = frame['stage']
        
        # 如果沒有圓盤需要移動，就直接跳過
        if curr_n == 0:
            continue
            
        if stage == 0:
            # 將自己重新推回 Stack，但將狀態改為 1 (下一次拿出來時就會印出移動指令)
            stack.append({'n': curr_n, 'src': src, 'aux': aux, 'tgt': tgt, 'stage': 1})
            
            # 模擬遞迴呼叫 hanoi(n-1, source, target, auxiliary)
            # 注意：因為是 Stack (後進先出)，要先執行的必須後放進去
            stack.append({'n': curr_n - 1, 'src': src, 'aux': tgt, 'tgt': aux, 'stage': 0})
            
        elif stage == 1:
            # 實際執行移動
            print(f"[非遞迴] 移動圓盤 {curr_n} : 從 {src} -> {tgt}")
            
            # 模擬遞迴呼叫 hanoi(n-1, auxiliary, source, target)
            stack.
