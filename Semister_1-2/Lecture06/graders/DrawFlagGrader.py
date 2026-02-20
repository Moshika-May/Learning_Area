import ast
import runpy
import signal
import sys
import types

TOLERANCE = 1e-6
TIMEOUT_SECONDS = 2
ACCEPTED_RED = {"red", "#ff0000"}
ALLOWED_LITERALS = {0, 1, 2}


class MockCanvas:
    instances = []

    def __init__(self, width=None, height=None, title=None):
        self.width = width
        self.height = height
        self.rectangles = []
        MockCanvas.instances.append(self)

    def create_rectangle(self, x1, y1, x2, y2, *args, **kwargs):
        fill = None
        if "color" in kwargs and kwargs["color"] is not None:
            fill = kwargs["color"]
        elif "fill" in kwargs and kwargs["fill"] is not None:
            fill = kwargs["fill"]
        elif len(args) >= 1:
            fill = args[0]
        self.rectangles.append({"coords": (x1, y1, x2, y2), "fill": fill})
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


def _normalize_color(color):
    if not isinstance(color, str):
        return None
    return color.strip().lower()


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


def _get_call_arg(call, index, name):
    if len(call.args) > index:
        return call.args[index]
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    return None


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
        failures.append("Define constants for canvas size (module-level variables).")
        return False, failures

    canvas_calls = []
    rect_calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "Canvas":
            canvas_calls.append(node)
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "Canvas":
            canvas_calls.append(node)
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "create_rectangle":
            rect_calls.append(node)

    if not canvas_calls:
        failures.append("Did not find a Canvas(...) call.")
    else:
        ok = False
        for call in canvas_calls:
            width_arg = _get_call_arg(call, 0, "width")
            height_arg = _get_call_arg(call, 1, "height")
            if _has_disallowed_literal(width_arg) or not _uses_only_allowed_names(width_arg, module_names):
                continue
            if _has_disallowed_literal(height_arg) or not _uses_only_allowed_names(height_arg, module_names):
                continue
            ok = True
            break
        if not ok:
            failures.append("Canvas width/height should use named constants (no magic numbers).")

    if not rect_calls:
        failures.append("Did not find any call to create_rectangle(...).")
    else:
        ok = False
        for call in rect_calls:
            coords = [_get_call_arg(call, i, name) for i, name in enumerate(["x1", "y1", "x2", "y2"])]
            if len(coords) < 4 or any(c is None for c in coords):
                failures.append("Rectangle must include x1, y1, x2, y2 coordinates.")
                continue
            if any(_has_disallowed_literal(coord) for coord in coords):
                continue
            if all(_uses_only_allowed_names(coord, module_names) for coord in coords):
                ok = True
                break
        if not ok:
            failures.append("Rectangle coordinates should be derived from constants (no magic numbers).")

    if failures:
        return False, failures
    return True, []


def _check_flag(canvas):
    width = _to_float(canvas.width)
    height = _to_float(canvas.height)
    if width is None or height is None:
        return False, "Canvas width/height must be numeric."

    expected_half = height / 2.0

    for rect in canvas.rectangles:
        norm = _normalize_rect(rect["coords"])
        if norm is None:
            continue
        left, top, right, bottom = norm
        fill = _normalize_color(rect.get("fill"))
        if fill not in ACCEPTED_RED:
            continue
        if _is_close(left, 0) and _is_close(top, 0) and _is_close(right, width) and _is_close(
            bottom, expected_half
        ):
            return True, "Success"

    return False, "Did not find a red rectangle covering the top half of the canvas."


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
    ok, msg = _check_flag(canvas)
    if not ok:
        return 0, [msg]

    return 100, ["Great job! Your DrawFlag program draws the Indonesia flag correctly."]
