"""
Lambda Calculus Interpreter in Python
這是一個支援具名變數、正規序化簡與變數防捕捉機制的 Lambda 運算解譯器。
"""

class Term:
    pass

class Var(Term):
    """變數，例如: x"""
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return self.name

class Abs(Term):
    """抽象化（函數定義），例如: λx. x"""
    def __init__(self, param: str, body: Term):
        self.param = param
        self.body = body
    def __repr__(self):
        return f"(λ{self.param}. {self.body})"

class App(Term):
    """應用（函數呼叫），例如: (f x)"""
    def __init__(self, func: Term, arg: Term):
        self.func = func
        self.arg = arg
    def __repr__(self):
        return f"({self.func} {self.arg})"


def free_vars(term: Term) -> set:
    """計算自由變數 (Free Variables)"""
    if isinstance(term, Var):
        return {term.name}
    elif isinstance(term, Abs):
        fv = free_vars(term.body)
        fv.discard(term.param)
        return fv
    elif isinstance(term, App):
        return free_vars(term.func) | free_vars(term.arg)
    return set()


def fresh_var(name: str, existing_vars: set) -> str:
    """產生不會衝突的新變數名稱（用於 α-轉換）"""
    if name not in existing_vars:
        return name
    i = 1
    while f"{name}{i}" in existing_vars:
        i += 1
    return f"{name}{i}"


def substitute(term: Term, var_name: str, replacement: Term) -> Term:
    """執行變數取代 (Substitution)，具備防捕捉機制"""
    if isinstance(term, Var):
        return replacement if term.name == var_name else term
    
    elif isinstance(term, Abs):
        if term.param == var_name:
            return term  # 參數被遮蔽（Shadowing）
        
        fv_rep = free_vars(replacement)
        if term.param in fv_rep:
            # 發生變數衝突，進行 α-轉換
            all_vars = free_vars(term.body) | fv_rep | {var_name, term.param}
            new_param = fresh_var(term.param, all_vars)
            new_body = substitute(term.body, term.param, Var(new_param))
            return Abs(new_param, substitute(new_body, var_name, replacement))
        else:
            return Abs(term.param, substitute(term.body, var_name, replacement))
            
    elif isinstance(term, App):
        return App(
            substitute(term.func, var_name, replacement),
            substitute(term.arg, var_name, replacement)
        )
    return term


def reduce_normal_order(term: Term):
    """執行單一步驟的正規序化簡 (Normal-Order Reduction)"""
    if isinstance(term, App):
        # 1. 如果函數部分是抽象（Abs），則進行 Beta 歸約
        if isinstance(term.func, Abs):
            reduced = substitute(term.func.body, term.func.param, term.arg)
            return reduced, True
        
        # 2. 否則，先嘗試化簡函數部分
        new_func, changed = reduce_normal_order(term.func)
        if changed:
            return App(new_func, term.arg), True
        
        # 3. 函數無法化簡時，嘗試化簡引數部分
        new_arg, changed = reduce_normal_order(term.arg)
        if changed:
            return App(term.func, new_arg), True
            
    elif isinstance(term, Abs):
        new_body, changed = reduce_normal_order(term.body)
        if changed:
            return Abs(term.param, new_body), True
            
    return term, False


def evaluate(term: Term) -> Term:
    """完整評估運算式，並印出每一步的計算過程"""
    current = term
    print(f"初始運算式: {current}")
    step = 1
    while True:
        nxt, changed = reduce_normal_order(current)
        if not changed:
            break
        print(f"步驟 {step}: {nxt}")
        current = nxt
        step += 1
    print(f"最終結果: {current}\n" + "-"*40)
    return current


if __name__ == "__main__":
    print("=== 範例 1: 簡單的恆等函數應用 ===")
    # 運算式: (λx. x) y
    expr1 = App(Abs("x", Var("x")), Var("y"))
    evaluate(expr1)

    print("=== 範例 2: 巢狀函數與應用 ===")
    # 運算式: (λx. λy. x) a b
    expr2 = App(App(Abs("x", Abs("y", Var("x"))), Var("a")), Var("b"))
    evaluate(expr2)

    print("=== 範例 3: 邱奇布林值 (Church Booleans - IF 邏輯) ===")
    # 定義 TRUE = λx. λy. x
    TRUE = Abs("x", Abs("y", Var("x")))
    # 定義 FALSE = λx. λy. y
    FALSE = Abs("x", Abs("y", Var("y")))
    # 定義 IF = λp. λa. λb. p a b
    IF = Abs("p", Abs("a", Abs("b", App(App(Var("p"), Var("a")), Var("b")))))
    
    # 運算式: IF TRUE a b -> 應該要選出 a
    expr3 = App(App(App(IF, TRUE), Var("a")), Var("b"))
    evaluate(expr3)
