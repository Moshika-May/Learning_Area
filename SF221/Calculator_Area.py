import ast
import operator as op
import tkinter as tk
from tkinter import messagebox
import math


ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def eval_expr(expr):
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError:
        raise ValueError("Invalid equation")
    return _eval(tree.body)


def _eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPS:
            raise ValueError("Unsupported operator")
        return ALLOWED_OPS[op_type](_eval(node.left), _eval(node.right))

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPS:
            raise ValueError("Unsupported operator")
        return ALLOWED_OPS[op_type](_eval(node.operand))

    raise ValueError("Unsupported expression")


def button_style(char):
    if char.isdigit() or char == ".":
        return {}

    if char in ("(", ")"):
        return {"bg": "#c8d6e5", "activebackground": "#dfe6e9"}

    if char in ("+", "-", "*", "/", "//", "%", "**"):
        return {"bg": "#54a0ff", "activebackground": "#74b9ff"}

    if char == "C":
        return {"bg": "#ff6b6b", "activebackground": "#ff8787"}

    if char == "⌫":
        return {"bg": "#feca57", "activebackground": "#ffdf8e"}

    if char == "=":
        return {"bg": "#1dd1a1", "activebackground": "#33e6b5"}

    if char == "Hist":
        return {"bg": "#9b59b6", "activebackground": "#af7ac5"}

    if char == "Area":
        return {"bg": "#10ac84", "activebackground": "#1dd1a1"}

    return {}


def press(char):
    if char == "C":
        current.set("")
    elif char == "⌫":
        current.set(current.get()[:-1])
    elif char == "Hist":
        toggle_history()
    elif char == "Area":
        area_window()
    elif char == "=":
        calculate()
    else:
        current.set(current.get() + char)


def calculate(event=None):
    expr = current.get().strip()
    if not expr:
        return

    try:
        result = eval_expr(expr)
    except ZeroDivisionError:
        messagebox.showerror("Math error", "Division by zero is not allowed.")
        return
    except Exception as e:
        messagebox.showerror("Invalid equation", str(e))
        return

    text = f"{expr} = {result}"
    history.append(text)
    result_label.config(text=text)
    history_list.insert(tk.END, text)
    current.set(str(result))


# -----------------------------
# คำนวณพื้นที่
# -----------------------------

def area_window():
    window = tk.Toplevel(root)
    window.title("Area Calculator")
    window.resizable(False, False)

    tk.Label(
        window,
        text="เลือกพื้นที่ที่ต้องการคำนวณ",
        font=("Arial", 14)
    ).pack(pady=10)

    tk.Button(
        window,
        text="สี่เหลี่ยมผืนผ้า",
        width=25,
        command=lambda: rectangle_area(window)
    ).pack(pady=3)

    tk.Button(
        window,
        text="สี่เหลี่ยมจัตุรัส",
        width=25,
        command=lambda: square_area(window)
    ).pack(pady=3)

    tk.Button(
        window,
        text="สามเหลี่ยม",
        width=25,
        command=lambda: triangle_area(window)
    ).pack(pady=3)

    tk.Button(
        window,
        text="วงกลม",
        width=25,
        command=lambda: circle_area(window)
    ).pack(pady=3)

    tk.Button(
        window,
        text="สี่เหลี่ยมคางหมู",
        width=25,
        command=lambda: trapezoid_area(window)
    ).pack(pady=3)


def rectangle_area(parent):
    window = tk.Toplevel(parent)
    window.title("พื้นที่สี่เหลี่ยมผืนผ้า")

    tk.Label(window, text="ความยาว").pack()
    length = tk.Entry(window)
    length.pack()

    tk.Label(window, text="ความกว้าง").pack()
    width = tk.Entry(window)
    width.pack()

    result = tk.Label(window, text="")
    result.pack(pady=10)

    def calculate_area():
        try:
            l = float(length.get())
            w = float(width.get())
            area = l * w
            result.config(text=f"พื้นที่ = {area}")
        except ValueError:
            messagebox.showerror("Error", "กรุณาใส่ตัวเลข")

    tk.Button(window, text="คำนวณ", command=calculate_area).pack()


def square_area(parent):
    window = tk.Toplevel(parent)
    window.title("พื้นที่สี่เหลี่ยมจัตุรัส")

    tk.Label(window, text="ความยาวด้าน").pack()
    side = tk.Entry(window)
    side.pack()

    result = tk.Label(window, text="")
    result.pack(pady=10)

    def calculate_area():
        try:
            s = float(side.get())
            area = s * s
            result.config(text=f"พื้นที่ = {area}")
        except ValueError:
            messagebox.showerror("Error", "กรุณาใส่ตัวเลข")

    tk.Button(window, text="คำนวณ", command=calculate_area).pack()


def triangle_area(parent):
    window = tk.Toplevel(parent)
    window.title("พื้นที่สามเหลี่ยม")

    tk.Label(window, text="ฐาน").pack()
    base = tk.Entry(window)
    base.pack()

    tk.Label(window, text="ความสูง").pack()
    height = tk.Entry(window)
    height.pack()

    result = tk.Label(window, text="")
    result.pack(pady=10)

    def calculate_area():
        try:
            b = float(base.get())
            h = float(height.get())
            area = 0.5 * b * h
            result.config(text=f"พื้นที่ = {area}")
        except ValueError:
            messagebox.showerror("Error", "กรุณาใส่ตัวเลข")

    tk.Button(window, text="คำนวณ", command=calculate_area).pack()


def circle_area(parent):
    window = tk.Toplevel(parent)
    window.title("พื้นที่วงกลม")

    tk.Label(window, text="รัศมี").pack()
    radius = tk.Entry(window)
    radius.pack()

    result = tk.Label(window, text="")
    result.pack(pady=10)

    def calculate_area():
        try:
            r = float(radius.get())
            area = math.pi * r * r
            result.config(text=f"พื้นที่ = {area:.2f}")
        except ValueError:
            messagebox.showerror("Error", "กรุณาใส่ตัวเลข")

    tk.Button(window, text="คำนวณ", command=calculate_area).pack()


def trapezoid_area(parent):
    window = tk.Toplevel(parent)
    window.title("พื้นที่สี่เหลี่ยมคางหมู")

    tk.Label(window, text="ฐานบน").pack()
    top = tk.Entry(window)
    top.pack()

    tk.Label(window, text="ฐานล่าง").pack()
    bottom = tk.Entry(window)
    bottom.pack()

    tk.Label(window, text="ความสูง").pack()
    height = tk.Entry(window)
    height.pack()

    result = tk.Label(window, text="")
    result.pack(pady=10)

    def calculate_area():
        try:
            a = float(top.get())
            b = float(bottom.get())
            h = float(height.get())
            area = ((a + b) * h) / 2
            result.config(text=f"พื้นที่ = {area}")
        except ValueError:
            messagebox.showerror("Error", "กรุณาใส่ตัวเลข")

    tk.Button(window, text="คำนวณ", command=calculate_area).pack()


# -----------------------------
# History
# -----------------------------

def clear_history():
    history.clear()
    history_list.delete(0, tk.END)
    result_label.config(text="")


def toggle_history():
    global history_visible

    if history_visible:
        history_frame.grid_remove()
    else:
        history_frame.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="n"
        )

    history_visible = not history_visible


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()
root.title("Calculator")
root.resizable(False, False)

history = []
history_visible = False
current = tk.StringVar()

calc_frame = tk.Frame(root)
calc_frame.grid(row=0, column=0, padx=10, pady=10)

display = tk.Entry(
    calc_frame,
    textvariable=current,
    justify="right",
    font=("Arial", 20),
    width=18
)

display.grid(
    row=0,
    column=0,
    columnspan=4,
    padx=5,
    pady=5,
    ipadx=5,
    ipady=5
)

display.bind("<Return>", calculate)

result_label = tk.Label(
    calc_frame,
    text="",
    font=("Arial", 10)
)

result_label.grid(
    row=1,
    column=0,
    columnspan=4
)

buttons = [
    ("(", ")", "C", "⌫"),
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
    ("0", ".", "=", "+"),
    ("%", "//", "**", "Hist"),
    ("Area", "Area", "Area", "Area")
]

for r, row in enumerate(buttons, start=2):
    for c, char in enumerate(row):
        tk.Button(
            calc_frame,
            text=char,
            font=("Arial", 14),
            width=5,
            height=2,
            command=lambda ch=char: press(ch),
            **button_style(char)
        ).grid(
            row=r,
            column=c,
            padx=3,
            pady=3
        )

history_frame = tk.Frame(root)

tk.Label(
    history_frame,
    text="History",
    font=("Arial", 12)
).pack(pady=(0, 5))

history_list = tk.Listbox(
    history_frame,
    width=25,
    height=15
)

history_list.pack(padx=5, pady=5)

tk.Button(
    history_frame,
    text="Clear",
    command=clear_history
).pack(pady=5)

root.mainloop()
