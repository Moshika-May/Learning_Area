import ast
import runpy
import signal
import sys
import types

TOLERANCE = 1e-6
TIMEOUT_SECONDS = 2
ALLOWED_LITERALS = {0, 1, 2, 3, 4}


class MockCanvas:
    instances = []

    def __init__(self, width=None, height=None, title=None):
        self.width = width
        self.height = height
        self.rectangles = []
        self.ovals = []
        self.mainloop_called = False
        MockCanvas.instances.append(self)

    def create_rectangle(self, x1, y1, x2, y2, *args, **kwargs):
        fill, outline = _extract_colors(args, kwargs)
        self.rectangles.append({"coords": (x1, y1, x2, y2), "fill": fill, "outline": outline})
        return None

    def create_oval(self, x1, y1, x2, y2, *args, **kwargs):
        fill, outline = _extract_colors(args, kwargs)
        self.ovals.append({"coords": (x1, y1, x2, y2), "fill": fill, "outline": outline})
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


def _extract_colors(args, kwargs):
    fill = None
    outline = None
    if "color" in kwargs and kwargs["color"] is not None:
        fill = kwargs["color"]
    if "fill" in kwargs and kwargs["fill"] is not None:
        fill = kwargs["fill"]
    if "outline" in kwargs and kwargs["outline"] is not None:
        outline = kwargs["outline"]
    if len(args) >= 1 and fill is None:
        fill = args[0]
    if len(args) >= 2 and outline is None:
        outline = args[1]
    return fill, outline


def _normalize_color(value):
    if not isinstance(value, str):
        return None
    return value.strip().lower()


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
        failures.append("Define constants for patch sizing (module-level variables).")
        return False, failures

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "Canvas":
                width_arg = _get_call_arg(node, 0, "width")
                height_arg = _get_call_arg(node, 1, "height")
                if _has_disallowed_literal(width_arg) or not _uses_only_allowed_names(width_arg, module_names):
                    failures.append("Canvas width should use a named constant (no magic numbers).")
                if _has_disallowed_literal(height_arg) or not _uses_only_allowed_names(height_arg, module_names):
                    failures.append("Canvas height should use a named constant (no magic numbers).")

    for func in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        allowed = _compute_allowed_names(func, module_names)
        for call in [n for n in ast.walk(func) if isinstance(n, ast.Call)]:
            if not isinstance(call.func, ast.Attribute):
                continue
            if call.func.attr not in {"create_rectangle", "create_oval"}:
                continue
            coords = [_get_call_arg(call, i, name) for i, name in enumerate(["x1", "y1", "x2", "y2"])]
            if len(coords) < 4 or any(c is None for c in coords):
                failures.append("Shape calls must include x1, y1, x2, y2 coordinates.")
                continue
            for coord in coords:
                if _has_disallowed_literal(coord):
                    failures.append("Shape coordinates should use constants (no magic numbers).")
                    break
                if not _uses_only_allowed_names(coord, allowed):
                    failures.append("Shape coordinates should be derived from constants and/or parameters.")
                    break

    if failures:
        return False, failures
    return True, []


def _snap_index(value, size):
    idx = round(value / size)
    if _is_close(value, idx * size):
        return idx
    return None


def _collect_patch_shapes(canvas):
    width = _to_float(canvas.width)
    height = _to_float(canvas.height)
    if width is None or height is None:
        return None, None, None, None, "Canvas width/height must be numeric."

    sizes = []
    for oval in canvas.ovals:
        norm = _normalize_rect(oval["coords"])
        if norm is None:
            continue
        left, top, right, bottom = norm
        w = right - left
        h = bottom - top
        if _is_close(w, h) and w > 0:
            sizes.append(w)
    for rect in canvas.rectangles:
        norm = _normalize_rect(rect["coords"])
        if norm is None:
            continue
        left, top, right, bottom = norm
        w = right - left
        h = bottom - top
        if _is_close(w, h) and w > 0:
            if _is_close(w, width) and _is_close(h, height):
                continue
            sizes.append(w)

    if not sizes:
        return None, None, None, None, "Did not find any square or circle patches."

    patch_size = max(sizes)

    cols = round(width / patch_size)
    rows = round(height / patch_size)
    if cols < 1 or rows < 1:
        return None, None, None, None, "Patch size does not fit the canvas."
    if not _is_close(width, cols * patch_size) or not _is_close(height, rows * patch_size):
        return None, None, None, None, "Canvas size should be a multiple of the patch size."

    circle_cells = {}
    square_cells = {}
    circle_colors = set()
    square_colors = set()

    for oval in canvas.ovals:
        norm = _normalize_rect(oval["coords"])
        if norm is None:
            continue
        left, top, right, bottom = norm
        w = right - left
        h = bottom - top
        if not (_is_close(w, patch_size) and _is_close(h, patch_size)):
            continue
        col = _snap_index(left, patch_size)
        row = _snap_index(top, patch_size)
        if col is None or row is None:
            continue
        circle_cells[(row, col)] = True
        color = _normalize_color(oval.get("fill")) or _normalize_color(oval.get("outline"))
        if color:
            circle_colors.add(color)

    for rect in canvas.rectangles:
        norm = _normalize_rect(rect["coords"])
        if norm is None:
            continue
        left, top, right, bottom = norm
        w = right - left
        h = bottom - top
        if not (_is_close(w, patch_size) and _is_close(h, patch_size)):
            continue
        col = _snap_index(left, patch_size)
        row = _snap_index(top, patch_size)
        if col is None or row is None:
            continue
        square_cells[(row, col)] = True
        color = _normalize_color(rect.get("fill")) or _normalize_color(rect.get("outline"))
        if color:
            square_colors.add(color)

    return (rows, cols, circle_cells, square_cells, (circle_colors, square_colors))


def _check_quilt_pattern(canvas):
    result = _collect_patch_shapes(canvas)
    if result is None:
        return False, "Could not analyze quilt shapes."
    rows, cols, circle_cells, square_cells, color_sets = result
    if rows is None:
        return False, cols

    if not circle_cells or not square_cells:
        return False, "Quilt should include both circle and square patches."

    for row in range(rows):
        for col in range(cols):
            has_circle = (row, col) in circle_cells
            has_square = (row, col) in square_cells
            if has_circle and has_square:
                return False, "A patch cell should not contain both a circle and a square."
            if not (has_circle or has_square):
                return False, "All patch cells should contain a circle or a square."

    def matches_checkerboard(circle_on_even):
        for row in range(rows):
            for col in range(cols):
                expect_circle = (row + col) % 2 == 0 if circle_on_even else (row + col) % 2 == 1
                has_circle = (row, col) in circle_cells
                if expect_circle != has_circle:
                    return False
        return True

    if not (matches_checkerboard(True) or matches_checkerboard(False)):
        return False, "Patches should alternate between circles and squares."

    circle_colors, square_colors = color_sets
    if not circle_colors or not square_colors:
        return False, "Circles and squares should use colors."
    if circle_colors == square_colors:
        return False, "Circle and square patches should use different colors."

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
    ok, msg = _check_quilt_pattern(canvas)
    if not ok:
        return 0, [msg]

    return 100, ["Great job! Your Quilt program draws the quilt pattern correctly."]
