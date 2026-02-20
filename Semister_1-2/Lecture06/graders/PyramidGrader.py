import ast
import runpy
import signal
import sys
import types

TOLERANCE = 1e-6
TIMEOUT_SECONDS = 2
ALLOWED_LITERALS = {0, 1, 2}


class MockCanvas:
    instances = []

    def __init__(self, width=None, height=None, title=None):
        self.width = width
        self.height = height
        self.rectangles = []
        self.mainloop_called = False
        MockCanvas.instances.append(self)

    def create_rectangle(self, x1, y1, x2, y2, *args, **kwargs):
        self.rectangles.append((x1, y1, x2, y2))
        return None

    def mainloop(self):
        self.mainloop_called = True
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


def _has_disallowed_literal(expr):
    if expr is None:
        return True
    for node in ast.walk(expr):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if abs(node.value) not in ALLOWED_LITERALS:
                return True
        elif isinstance(node, ast.Num):
            if abs(node.n) not in ALLOWED_LITERALS:
                return True
    return False


def _uses_only_allowed_names(expr, allowed_names):
    if expr is None:
        return False
    for node in ast.walk(expr):
        if isinstance(node, ast.Name) and node.id not in allowed_names:
            return False
    return True


def _expr_has_module_name(expr, module_names):
    if expr is None:
        return False
    for node in ast.walk(expr):
        if isinstance(node, ast.Name) and node.id in module_names:
            return True
    return False


def _expr_has_name(expr, name):
    if expr is None:
        return False
    for node in ast.walk(expr):
        if isinstance(node, ast.Name) and node.id == name:
            return True
    return False


def _get_call_arg(call, index, name):
    if len(call.args) > index:
        return call.args[index]
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    return None


def _collect_loop_vars(func_node):
    loop_vars = set()
    for node in ast.walk(func_node):
        if isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            loop_vars.add(node.target.id)
    return loop_vars


def _collect_assignments(func_node):
    assignments = []
    for node in ast.walk(func_node):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            assignments.append((node.targets[0].id, node.value))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            assignments.append((node.target.id, node.value))
    return assignments


def _compute_allowed_names(func_node, module_names):
    params = {arg.arg for arg in func_node.args.args}
    loop_vars = _collect_loop_vars(func_node)
    allowed = set(module_names) | params | loop_vars
    assignments = _collect_assignments(func_node)
    changed = True
    while changed:
        changed = False
        for name, expr in assignments:
            if name in allowed:
                continue
            if _has_disallowed_literal(expr):
                continue
            if _uses_only_allowed_names(expr, allowed):
                allowed.add(name)
                changed = True
    return allowed


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
        failures.append("Define constants for canvas and brick sizing (module-level variables).")
        return False, failures

    range_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "range":
            range_calls.append(node)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "Canvas":
                width_arg = _get_call_arg(node, 0, "width")
                height_arg = _get_call_arg(node, 1, "height")
                if _has_disallowed_literal(width_arg) or not _uses_only_allowed_names(width_arg, module_names):
                    failures.append("Canvas width should use a named constant (no magic numbers).")
                if _has_disallowed_literal(height_arg) or not _uses_only_allowed_names(height_arg, module_names):
                    failures.append("Canvas height should use a named constant (no magic numbers).")

    if not range_calls:
        failures.append("Did not find a loop using range(...).")
    else:
        ok = False
        found_magic_range = False
        for call in range_calls:
            args = call.args
            if not args:
                continue
            if any(_has_disallowed_literal(arg) for arg in args):
                found_magic_range = True
            if any(_expr_has_name(arg, "BRICKS_IN_BASE") for arg in args):
                if all(_has_disallowed_literal(arg) is False for arg in args):
                    ok = True
                    break
        if not ok:
            failures.append("BRICKS_IN_BASE should be used in a range(...) call.")
        if found_magic_range:
            failures.append("Do not use numeric literals in range(...); use BRICKS_IN_BASE (and other constants).")

    for func in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        allowed = _compute_allowed_names(func, module_names)
        for call in [n for n in ast.walk(func) if isinstance(n, ast.Call)]:
            if not isinstance(call.func, ast.Attribute):
                continue
            if call.func.attr != "create_rectangle":
                continue
            coords = [_get_call_arg(call, i, name) for i, name in enumerate(["x1", "y1", "x2", "y2"])]
            if len(coords) < 4 or any(c is None for c in coords):
                failures.append("Brick rectangles must include x1, y1, x2, y2 coordinates.")
                continue
            for coord in coords:
                if _has_disallowed_literal(coord):
                    failures.append("Brick coordinates should use constants (no magic numbers).")
                    break
                if not _uses_only_allowed_names(coord, allowed):
                    failures.append("Brick coordinates should be derived from constants and/or parameters.")
                    break

    if failures:
        return False, failures
    return True, []


def _choose_brick_size(bricks):
    counts = {}
    for left, top, right, bottom in bricks:
        width = right - left
        height = bottom - top
        if width <= 0 or height <= 0:
            continue
        key = (round(width, 4), round(height, 4))
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return None, None
    (bw, bh), _ = max(counts.items(), key=lambda item: item[1])
    return bw, bh


def _group_rows(bricks, brick_height):
    rows = []
    tol = max(TOLERANCE, brick_height * 0.05)
    for left, top, right, bottom in bricks:
        assigned = False
        for row in rows:
            if abs(top - row["top"]) <= tol:
                row["bricks"].append((left, top, right, bottom))
                assigned = True
                break
        if not assigned:
            rows.append({"top": top, "bricks": [(left, top, right, bottom)]})
    rows.sort(key=lambda r: r["top"], reverse=True)
    return rows


def _check_pyramid(canvas):
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

    brick_w, brick_h = _choose_brick_size(normalized)
    if brick_w is None or brick_h is None:
        return False, "Could not determine brick size."

    bricks = [
        r
        for r in normalized
        if _is_close(r[2] - r[0], brick_w) and _is_close(r[3] - r[1], brick_h)
    ]

    if not bricks:
        return False, "Did not find any bricks with consistent size."

    max_top = max(b[1] for b in bricks)
    max_bottom = max(b[3] for b in bricks)
    min_top = min(b[1] for b in bricks)
    if max_bottom > height + TOLERANCE or min_top < -TOLERANCE:
        return False, "Bricks should be drawn within the canvas height."
    if max_top > height - brick_h + max(TOLERANCE, brick_h * 0.05):
        return False, "Base row should sit on the bottom of the canvas (no bricks below the canvas)."

    rows = _group_rows(bricks, brick_h)
    if not rows:
        return False, "Could not group bricks into rows."

    base_row = rows[0]
    base_bottom = base_row["top"] + brick_h
    if abs(base_row["top"] - (height - brick_h)) > max(TOLERANCE, brick_h * 0.05):
        return False, "Base row should sit on the bottom of the canvas (no bricks below the canvas)."
    if abs(base_bottom - height) > brick_h + TOLERANCE:
        return False, "Pyramid should start from the bottom of the canvas."

    expected_count = len(base_row["bricks"])
    if expected_count < 1:
        return False, "Base row must contain at least one brick."

    center_target = width / 2.0
    center_tol = max(TOLERANCE, brick_w * 0.1)

    for idx, row in enumerate(rows):
        bricks_row = row["bricks"]
        bricks_row.sort(key=lambda b: b[0])

        for i in range(len(bricks_row) - 1):
            if abs(bricks_row[i][2] - bricks_row[i + 1][0]) > max(TOLERANCE, brick_w * 0.05):
                return False, "Bricks in a row should be adjacent with no gaps."

        min_left = bricks_row[0][0]
        max_right = bricks_row[-1][2]
        center = (min_left + max_right) / 2.0
        if abs(center - center_target) > center_tol:
            return False, "Each row should be centered on the canvas."

        if idx > 0:
            expected_count = expected_count - 1
            if expected_count <= 0:
                break
            if len(bricks_row) != expected_count:
                return False, "Each row should have one fewer brick than the row below it."

    return True, "Success"


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
    ok, msg = _check_pyramid(canvas)
    if not ok:
        return 0, [msg]

    return 100, ["Great job! Your Pyramid program draws the pyramid correctly."]
