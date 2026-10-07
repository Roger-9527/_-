def sym_diff(expr, var='x'):
    """
    遞迴求解符號數學式的微分
    
    語法樹結構 (AST)：
    - 常數：int / float，如 5, 3.14
    - 變數：str，如 'x', 'y'
    - 二元運算：(op, left, right)，如 ('+', 'x', 3)
    - 一元函數：(op, inner)，如 ('sin', 'x')
    """
    # ---------------------------------------------------------
    # 1. 基本條件 (Base Cases)
    # ---------------------------------------------------------
    # 常數微分為 0
    if isinstance(expr, (int, float)):
        return 0
    
    # 變數微分：若為目標變數則為 1，其餘變數視為常數 (0)
    if isinstance(expr, str):
        return 1 if expr == var else 0

    # ---------------------------------------------------------
    # 2. 遞迴條件 (Recursive Cases)
    # ---------------------------------------------------------
    if isinstance(expr, tuple):
        op = expr[0]
        
        # 加法法則：(f + g)' = f' + g'
        if op == '+':
            f, g = expr[1], expr[2]
            return ('+', sym_diff(f, var), sym_diff(g, var))
            
        # 減法法則：(f - g)' = f' - g'
        elif op == '-':
            f, g = expr[1], expr[2]
            return ('-', sym_diff(f, var), sym_diff(g, var))
            
        # 乘法法則：(f * g)' = f' * g + f * g'
        elif op == '*':
            f, g = expr[1], expr[2]
            return ('+', ('*', sym_diff(f, var), g), ('*', f, sym_diff(g, var)))
            
        # 除法法則：(f / g)' = (f' * g - f * g') / (g ^ 2)
        elif op == '/':
            f, g = expr[1], expr[2]
            num = ('-', ('*', sym_diff(f, var), g), ('*', f, sym_diff(g, var)))
            den = ('^', g, 2)
            return ('/', num, den)
            
        # 次方連鎖律（假設指數 n 為數值）：(u ^ n)' = n * (u ^ (n - 1)) * u'
        elif op == '^':
            u, n = expr[1], expr[2]
            return ('*', ('*', n, ('^', u, n - 1)), sym_diff(u, var))
            
        # 三角函數連鎖律：(sin(u))' = cos(u) * u'
        elif op == 'sin':
            u = expr[1]
            return ('*', ('cos', u), sym_diff(u, var))
            
        # 三角函數連鎖律：(cos(u))' = -1 * sin(u) * u'
        elif op == 'cos':
            u = expr[1]
            return ('*', -1, ('*', ('sin', u), sym_diff(u, var)))
            
        # 自然對數連鎖律：(ln(u))' = (1 / u) * u'
        elif op == 'ln':
            u = expr[1]
            return ('*', ('/', 1, u), sym_diff(u, var))

    raise ValueError(f"無法解析的數學運算式: {expr}")


def to_string(expr):
    """輔助函式：將 AST 轉為易讀的字串格式"""
    if isinstance(expr, (int, float, str)):
        return str(expr)
    
    op = expr[0]
    if op in ('+', '-', '*', '/', '^'):
        left = to_string(expr[1])
        right = to_string(expr[2])
        return f"({left} {op} {right})"
    elif op in ('sin', 'cos', 'ln'):
        inner = to_string(expr[1])
        return f"{op}({inner})"


if __name__ == "__main__":
    # 範例 1: f(x) = x^3 + 5*x
    # AST 表示：('+', ('^', 'x', 3), ('*', 5, 'x'))
    expr1 = ('+', ('^', 'x', 3), ('*', 5, 'x'))
    diff1 = sym_diff(expr1, var='x')
    print("原式 1 :", to_string(expr1))
    print("微分結果:", to_string(diff1))
    
    print("-" * 50)
    
    # 範例 2: f(x) = sin(x^2)
    # AST 表示：('sin', ('^', 'x', 2))
    expr2 = ('sin', ('^', 'x', 2))
    diff2 = sym_diff(expr2, var='x')
    print("原式 2 :", to_string(expr2))
    print("微分結果:", to_string(diff2))
