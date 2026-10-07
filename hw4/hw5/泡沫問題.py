# =========================================================
# 1. 自製高階函數 (無迴圈，純遞迴實作)
# =========================================================

def my_map(func, iterable):
    """自製 map 函數"""
    if not iterable:
        return []
    return [func(iterable[0])] + my_map(func, iterable[1:])


def my_filter(func, iterable):
    """自製 filter 函數"""
    if not iterable:
        return []
    head, tail = iterable[0], iterable[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    return my_filter(func, tail)


def my_reduce(func, iterable, initializer=None):
    """自製 reduce 函數"""
    if initializer is None:
        if not iterable:
            raise TypeError("my_reduce() of empty sequence with no initial value")
        return my_reduce(func, iterable[1:], iterable[0])
    if not iterable:
        return initializer
    return my_reduce(func, iterable[1:], func(initializer, iterable[0]))


# =========================================================
# 2. 禁止迴圈的泡沫排序 (Bubble Sort)
# =========================================================

def _bubble_step(acc, x):
    """
    單步比較與交換邏輯：
    acc 的最後一個元素為目前「持有的較大值」，若比目前的 x 大則進行交換。
    """
    if not acc:
        return [x]
    if acc[-1] > x:
        # 前數比 x 大：將 x 放在前面，較大數留在末端繼續往後浮游
        return acc[:-1] + [x, acc[-1]]
    else:
        # 前數 <= x：將 x 放在末端成為新的最大值
        return acc + [x]


def bubble_pass(lst):
    """內層迴圈替代方案：利用 my_reduce 完成單輪「大數往後浮游」"""
    return my_reduce(_bubble_step, lst, [])


def bubble_sort(lst, passes=None):
    """外層迴圈替代方案：利用遞迴執行 N 次 bubble_pass"""
    if passes is None:
        passes = len(lst)
    if passes <= 1 or len(lst) <= 1:
        return lst
    
    # 進行一輪浮游後，遞迴呼叫處理下一輪
    return bubble_sort(bubble_pass(lst), passes - 1)


# =========================================================
# 3. 測試與驗證
# =========================================================

if __name__ == "__main__":
    # --- 測試自製 map, filter, reduce ---
    nums = [1, 2, 3, 4, 5]
    
    squared = my_map(lambda x: x ** 2, nums)
    evens = my_filter(lambda x: x % 2 == 0, nums)
    total = my_reduce(lambda acc, x: acc + x, nums, 0)
    
    print("=== 1. 自製函數測試 ===")
    print("my_map (平方)   :", squared)  # [1, 4, 9, 16, 25]
    print("my_filter (偶數):", evens)    # [2, 4]
    print("my_reduce (總和):", total)    # 15

    # --- 測試無迴圈泡沫排序 ---
    unsorted_list = [64, 34, 25, 12, 22, 11, 90]
    sorted_list = bubble_sort(unsorted_list)
    
    print("\n=== 2. 無迴圈泡沫排序測試 ===")
    print("原始陣列:", unsorted_list)
    print("排序結果:", sorted_list)     # [11, 12, 22, 25, 34, 64, 90]
