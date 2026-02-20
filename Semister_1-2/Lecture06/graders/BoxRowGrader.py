import ast
import runpy
import signal
import sys
import types

TOLERANCE = 1e-6
TIMEOUT_SECONDS = 2


class MockCanvas:
    instances = []

    def __init__(self, width=None, height=None, title=None):
        self.width = width
        self.height = height
        self.rectangles = []
        MockCanvas.instances.append(self)

    def create_rectangle(self, x1, y1, x2, y2, *args, **kwargs):
        self.rectangles.append((x1, y1, x2, y2))
        return None

    def mainloop(self):
        return None

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def __getattr__(self, name):
        def _noop(*args, **kwargs):
            return None

        return _noop


class TimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError("Program timed out.")


def _is_number(value):
    return isinstance(value, (int, float))


def _to_float(value):
    if _is_number(value):
        return float(value)
    return None


def _is_close(a, b, tol=TOLERANCE):
    return a is not None and b is not None and abs(a - b) <= tol


def _normalize_rect(rect):
    x1, y1, x2, y2 = rect
    x1f = _to_float(x1)
    y1f = _to_float(y1)
    x2f = _to_float(x2)
    y2f = _to_float(y2)
    if None in (x1f, y1f, x2f, y2f):
        return None
    left = min(x1f, x2f)
    right = max(x1f, x2f)
    top = min(y1f, y2f)
    bottom = max(y1f, y2f)
    return (left, top, right, bottom)


def _run_student(student_file):
    fake_graphics = types.ModuleType("graphics")
    fake_graphics.Canvas = MockCanvas

    old_graphics = sys.modules.get("graphics")
    sys.modules["graphics"] = fake_graphics

    MockCanvas.instances = []

    has_alarm = hasattr(signal, "SIGALRM")
    if has_alarm:
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(TIMEOUT_SECONDS)

    try:
        runpy.run_path(student_file, run_name="__main__")
    finally:
        if has_alarm:
            signal.alarm(0)
        if old_graphics is not None:
            sys.modules["graphics"] = old_graphics
        else:
            sys.modules.pop("graphics", None)


def _has_name(expr, names):
    if expr is None:
        return False
    for node in ast.walk(expr):
        if isinstance(node, ast.Name) and node.id in names:
            return True
    return False


def _eval_numeric_expr(expr):
    if isinstance(expr, ast.Constant) and isinstance(expr.value, (int, float)):
        return float(expr.value), True
    if isinstance(expr, ast.Num):
        return float(expr.n), True
    if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, (ast.UAdd, ast.USub)):
        val, ok = _eval_numeric_expr(expr.operand)
        if ok:
            return (val if isinstance(expr.op, ast.UAdd) else -val), True
    if isinstance(expr, ast.BinOp):
        left, ok_l = _eval_numeric_expr(expr.left)
        right, ok_r = _eval_numeric_expr(expr.right)
        if ok_l and ok_r:
            if isinstance(expr.op, ast.Add):
                return left + right, True
            if isinstance(expr.op, ast.Sub):
                return left - right, True
            if isinstance(expr.op, ast.Mult):
                return left * right, True
            if isinstance(expr.op, ast.Div):
                return left / right, True
            if isinstance(expr.op, ast.FloorDiv):
                return left // right, True
    return None, False


def _has_disallowed_literal(expr):
    for node in ast.walk(expr):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if abs(node.value) not in (0, 1):
                return True
        elif isinstance(node, ast.Num):
            if abs(node.n) not in (0, 1):
                return True
    val, ok = _eval_numeric_expr(expr)
    if ok and abs(val) not in (0, 1):
        return True
    return False


def _is_expr_ok(expr, required_names, allow_literal_zero_one):
    if expr is None:
        return False
    if _has_disallowed_literal(expr):
        return False
    if _has_name(expr, required_names):
        return True
    if allow_literal_zero_one:
        val, ok = _eval_numeric_expr(expr)
        return ok and abs(val) in (0, 1)
    return False


def _get_call_arg(call, index, name):
    if len(call.args) > index:
        return call.args[index]
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    return None


def _get_rect_coords(call):
    coords = []
    for idx, name in enumerate(["x1", "y1", "x2", "y2"]):
        coords.append(_get_call_arg(call, idx, name))
    return coords


def _static_constants_check(student_file):
    try:
        with open(student_file, "r") as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        return False, [f"Error parsing code: {e}"]

    module_names = set()
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    module_names.add(target.id)
        elif isinstance(stmt, ast.AnnAssign):
            if isinstance(stmt.target, ast.Name):
                module_names.add(stmt.target.id)

    failures = []
    if not module_names:
        failures.append("Define constants for canvas size and square sizing (module-level variables).")
        return False, failures

    loop_vars = set()
    range_calls = []
    canvas_calls = []
    rect_calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            loop_vars.add(node.target.id)
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "Canvas":
            canvas_calls.append(node)
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "Canvas":
            canvas_calls.append(node)
        elif isinstance(node.func, ast.Name) and node.func.id == "range":
            range_calls.append(node)
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "create_rectangle":
            rect_calls.append(node)

    if not canvas_calls:
        failures.append("Did not find a Canvas(...) call.")
    else:
        ok = False
        for call in canvas_calls:
            width_arg = _get_call_arg(call, 0, "width")
            height_arg = _get_call_arg(call, 1, "height")
            if _is_expr_ok(width_arg, module_names, allow_literal_zero_one=False) and _is_expr_ok(
                height_arg, module_names, allow_literal_zero_one=False
            ):
                ok = True
                break
        if not ok:
            failures.append("Canvas width/height should use named constants (not numeric literals).")

    if not range_calls:
        failures.append("Did not find a loop using range(...).")
    else:
        ok = False
        for call in range_calls:
            args = call.args
            if len(args) == 1:
                if _is_expr_ok(args[0], module_names, allow_literal_zero_one=False):
                    ok = True
            elif len(args) >= 2:
                start_ok = _is_expr_ok(args[0], set(), allow_literal_zero_one=True)
                end_ok = _is_expr_ok(args[1], module_names, allow_literal_zero_one=False)
                step_ok = True
                if len(args) >= 3:
                    step_ok = _is_expr_ok(args[2], set(), allow_literal_zero_one=True) or _is_expr_ok(
                        args[2], module_names, allow_literal_zero_one=False
                    )
                if start_ok and end_ok and step_ok:
                    ok = True
            if ok:
                break
        if not ok:
            failures.append("range(...) should use a named constant for the number of squares (not a numeric literal).")

    if not rect_calls:
        failures.append("Did not find any call to create_rectangle(...).")
    else:
        ok = False
        allowed_names = set(module_names) | set(loop_vars)
        for call in rect_calls:
            coords = _get_rect_coords(call)
            if len(coords) >= 4 and all(_is_expr_ok(arg, allowed_names, allow_literal_zero_one=True) for arg in coords):
                ok = True
                break
        if not ok:
            failures.append(
                "Rectangle coordinates should be derived from named constants and/or the loop variable (no magic numbers)."
            )

    if failures:
        return False, failures
    return True, []


def _check_visual_output(canvas):
    width = _to_float(canvas.width)
    height = _to_float(canvas.height)
    if width is None or height is None:
        return False, "Canvas width/height must be numeric."

    normalized = []
    for rect in canvas.rectangles:
        norm = _normalize_rect(rect)
        if norm is not None:
            normalized.append(norm)

    if not normalized:
        return False, "Did not find any rectangles."

    bottom_squares = []
    for left, top, right, bottom in normalized:
        if _is_close(bottom, height):
            rect_w = right - left
            rect_h = bottom - top
            if _is_close(rect_w, rect_h) and rect_w > 0:
                if _is_close(top, height - rect_h):
                    bottom_squares.append((left, top, right, bottom, rect_w))

    if not bottom_squares:
        return False, "Did not find any square on the bottom row."

    for _, _, _, _, size in bottom_squares:
        group = [r for r in bottom_squares if _is_close(r[4], size)]
        if not group:
            continue
        group.sort(key=lambda r: r[0])
        if not _is_close(group[0][0], 0):
            continue
        ok = True
        for i in range(len(group) - 1):
            if not _is_close(group[i][2], group[i + 1][0]):
                ok = False
                break
        if not ok:
            continue
        if not _is_close(group[-1][2], width):
            continue
        return True, "Success"

    return False, "Squares should form a continuous row across the bottom of the canvas."


def grade(student_file):
    ok, feedback = _static_constants_check(student_file)
    if not ok:
        return 0, feedback

    try:
        _run_student(student_file)
    except TimeoutError as e:
        return 0, [str(e)]
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 0
        if code != 0:
            return 0, [f"Program exited early with code {code}."]
    except Exception as e:
        return 0, [f"Error running program: {e}"]

    if not MockCanvas.instances:
        return 0, ["Did not create a Canvas."]

    canvas = MockCanvas.instances[0]
    ok, msg = _check_visual_output(canvas)
    if not ok:
        return 0, [msg]

    return 100, ["Great job! Your BoxRow program draws the row of squares correctly."]
