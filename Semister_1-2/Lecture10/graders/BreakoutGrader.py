import ast
import runpy
import signal
import sys
import types

TOLERANCE = 1e-6
TIMEOUT_SECONDS = 2

REQUIRED_CONSTANTS = {
    "CANVAS_WIDTH",
    "CANVAS_HEIGHT",
    "N_BRICK_COLUMNS",
    "N_BRICK_ROWS",
    "BRICK_SEP",
    "BRICK_WIDTH",
    "BRICK_HEIGHT",
    "BRICK_Y_OFFSET",
    "COLORS",
    "BALL_RADIUS",
    "VELOCITY_Y",
    "VELOCITY_X_MIN",
    "VELOCITY_X_MAX",
    "DELAY",
    "PADDLE_WIDTH",
    "PADDLE_HEIGHT",
    "PADDLE_Y_OFFSET",
    "N_TURNS",
}

REQUIRED_FUNCTIONS = {"create_bricks", "create_ball", "create_paddle", "main"}


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


def _normalize_color(value):
    if not isinstance(value, str):
        return None
    return value.strip().lower()


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


class MockCanvas:
    instances = []

    def __init__(self, width=None, height=None, title=None):
        self.width = width
        self.height = height
        self.title = title
        self.background = None
        self.mouse_x = 0
        self.mainloop_called = False
        self.update_calls = 0
        self.wait_for_click_calls = 0
        self._next_id = 1
        self._objects = {}
        MockCanvas.instances.append(self)

    def _create_shape(self, shape_type, coords, **extra):
        obj_id = self._next_id
        self._next_id += 1
        self._objects[obj_id] = {
            "type": shape_type,
            "coords": [float(value) for value in coords],
            **extra,
        }
        return obj_id

    def create_rectangle(self, x1, y1, x2, y2, *args, **kwargs):
        fill, outline = _extract_colors(args, kwargs)
        return self._create_shape(
            "rectangle",
            [x1, y1, x2, y2],
            fill=fill,
            outline=outline,
        )

    def create_oval(self, x1, y1, x2, y2, *args, **kwargs):
        fill, outline = _extract_colors(args, kwargs)
        return self._create_shape(
            "oval",
            [x1, y1, x2, y2],
            fill=fill,
            outline=outline,
        )

    def create_text(self, x, y, text="", fill="black", anchor="nw", color=None, **kwargs):
        if color is not None:
            fill = color
        return self._create_shape(
            "text",
            [x, y],
            text=text,
            fill=fill,
            anchor=anchor,
        )

    def coords(self, obj, *newcoords):
        if obj not in self._objects:
            raise KeyError(f"Unknown canvas object: {obj}")
        if newcoords:
            self._objects[obj]["coords"] = [float(value) for value in newcoords]
        return tuple(self._objects[obj]["coords"])

    def move(self, obj, dx, dy):
        coords = list(self.coords(obj))
        if len(coords) == 4:
            coords[0] += dx
            coords[1] += dy
            coords[2] += dx
            coords[3] += dy
        elif len(coords) == 2:
            coords[0] += dx
            coords[1] += dy
        self.coords(obj, *coords)

    def move_to(self, obj, new_x, new_y):
        left_x = self.get_left_x(obj)
        top_y = self.get_top_y(obj)
        self.move(obj, new_x - left_x, new_y - top_y)

    def get_left_x(self, obj):
        coords = self.coords(obj)
        if len(coords) == 2:
            return coords[0]
        return coords[0]

    def get_top_y(self, obj):
        coords = self.coords(obj)
        if len(coords) == 2:
            return coords[1]
        return coords[1]

    def get_obj_width(self, obj):
        coords = self.coords(obj)
        if len(coords) == 2:
            return 0
        return coords[2] - coords[0]

    def get_obj_height(self, obj):
        coords = self.coords(obj)
        if len(coords) == 2:
            return 0
        return coords[3] - coords[1]

    def delete(self, obj):
        self._objects.pop(obj, None)

    def clear(self):
        self._objects.clear()

    def find_overlapping(self, x1, y1, x2, y2):
        results = []
        left = min(float(x1), float(x2))
        right = max(float(x1), float(x2))
        top = min(float(y1), float(y2))
        bottom = max(float(y1), float(y2))

        for obj_id, data in self._objects.items():
            bbox = _shape_bbox(data)
            if bbox is None:
                continue
            obj_left, obj_top, obj_right, obj_bottom = bbox
            if obj_right < left or right < obj_left or obj_bottom < top or bottom < obj_top:
                continue
            results.append(obj_id)
        return tuple(results)

    def set_canvas_background_fill(self, fill):
        self.background = fill

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_mouse_x(self):
        return self.mouse_x

    def update(self):
        self.update_calls += 1

    def wait_for_click(self):
        self.wait_for_click_calls += 1

    def mainloop(self):
        self.mainloop_called = True

    def __getattr__(self, name):
        def _noop(*args, **kwargs):
            return None

        return _noop


def _shape_bbox(shape):
    coords = shape["coords"]
    if len(coords) == 4:
        left = min(coords[0], coords[2])
        right = max(coords[0], coords[2])
        top = min(coords[1], coords[3])
        bottom = max(coords[1], coords[3])
        return left, top, right, bottom
    if len(coords) == 2:
        return coords[0], coords[1], coords[0], coords[1]
    return None


def _get_shapes(canvas, shape_type=None):
    items = []
    for obj_id in sorted(canvas._objects):
        data = canvas._objects[obj_id]
        if shape_type is None or data["type"] == shape_type:
            items.append((obj_id, data))
    return items


def _parse_tree(student_file):
    with open(student_file, "r") as f:
        source = f.read()
    return ast.parse(source)


def _load_student_namespace(student_file):
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
        return runpy.run_path(student_file, run_name="student_module")
    finally:
        if has_alarm:
            signal.alarm(0)
        if old_graphics is not None:
            sys.modules["graphics"] = old_graphics
        else:
            sys.modules.pop("graphics", None)


def _call_name(call):
    func = call.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _test_static_api(tree):
    points = 0
    feedback = []

    module_names = set()
    function_names = set()
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    module_names.add(target.id)
        elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            module_names.add(stmt.target.id)
        elif isinstance(stmt, ast.FunctionDef):
            function_names.add(stmt.name)

    missing_constants = sorted(REQUIRED_CONSTANTS - module_names)
    if not missing_constants:
        points += 8
    else:
        feedback.append("Missing required constants: " + ", ".join(missing_constants))

    missing_functions = sorted(REQUIRED_FUNCTIONS - function_names)
    if not missing_functions:
        points += 7
    else:
        feedback.append("Missing required functions: " + ", ".join(missing_functions))

    return points, 15, feedback


def _test_gameplay_signals(tree):
    points = 0
    feedback = []

    function_map = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    main_node = function_map.get("main")
    if main_node is None:
        return 0, 20, ["Missing main() function."]

    all_calls = [_call_name(node) for node in ast.walk(tree) if isinstance(node, ast.Call)]

    has_while = any(isinstance(node, ast.While) for node in ast.walk(main_node))
    if has_while:
        points += 4
    else:
        feedback.append("main() should contain a game loop.")

    if "wait_for_click" in all_calls:
        points += 4
    else:
        feedback.append("I didn't see a click-to-start step such as canvas.wait_for_click().")

    if "get_mouse_x" in all_calls:
        points += 4
    else:
        feedback.append("I didn't see paddle control based on the mouse x-position.")

    if any(name in all_calls for name in {"move", "move_to", "coords"}):
        points += 4
    else:
        feedback.append("I didn't see code that updates object positions during play.")

    if "find_overlapping" in all_calls and "delete" in all_calls:
        points += 4
    else:
        feedback.append("I didn't see both collision detection and brick removal in the program.")

    return points, 20, feedback


def _test_create_bricks(namespace):
    if not callable(namespace.get("create_bricks")):
        return 0, 30, ["create_bricks(canvas) is missing or not callable."]

    required_names = [
        "CANVAS_WIDTH",
        "CANVAS_HEIGHT",
        "N_BRICK_COLUMNS",
        "N_BRICK_ROWS",
        "BRICK_SEP",
        "BRICK_WIDTH",
        "BRICK_HEIGHT",
        "BRICK_Y_OFFSET",
        "COLORS",
    ]
    missing = [name for name in required_names if name not in namespace]
    if missing:
        return 0, 30, ["Missing constants needed to test brick creation: " + ", ".join(missing)]

    canvas = MockCanvas(namespace["CANVAS_WIDTH"], namespace["CANVAS_HEIGHT"], "Breakout")
    try:
        namespace["create_bricks"](canvas)
    except Exception as e:
        return 0, 30, [f"create_bricks(canvas) raised an error: {e}"]

    rectangles = _get_shapes(canvas, "rectangle")
    expected_count = namespace["N_BRICK_ROWS"] * namespace["N_BRICK_COLUMNS"]
    points = 0
    feedback = []

    if len(rectangles) == expected_count:
        points += 10
    else:
        feedback.append(
            f"create_bricks() should draw {expected_count} bricks, but I found {len(rectangles)}."
        )

    coords_ok = True
    colors_ok = True
    in_bounds_ok = True

    expected_colors = namespace["COLORS"]
    if not isinstance(expected_colors, (list, tuple)) or len(expected_colors) < max(1, namespace["N_BRICK_ROWS"] // 2):
        colors_ok = False
    else:
        expected_colors = [_normalize_color(color) for color in expected_colors]

    for index, (_, rect) in enumerate(rectangles):
        row = index // namespace["N_BRICK_COLUMNS"]
        col = index % namespace["N_BRICK_COLUMNS"]
        left_x = namespace["BRICK_SEP"] + col * (namespace["BRICK_WIDTH"] + namespace["BRICK_SEP"])
        top_y = namespace["BRICK_Y_OFFSET"] + row * (namespace["BRICK_HEIGHT"] + namespace["BRICK_SEP"])
        right_x = left_x + namespace["BRICK_WIDTH"]
        bottom_y = top_y + namespace["BRICK_HEIGHT"]
        actual = rect["coords"]

        if len(actual) != 4:
            coords_ok = False
            in_bounds_ok = False
            continue

        if not (
            _is_close(actual[0], left_x)
            and _is_close(actual[1], top_y)
            and _is_close(actual[2], right_x)
            and _is_close(actual[3], bottom_y)
        ):
            coords_ok = False

        if not (
            actual[0] >= -TOLERANCE
            and actual[1] >= -TOLERANCE
            and actual[2] <= namespace["CANVAS_WIDTH"] + TOLERANCE
            and actual[3] <= namespace["CANVAS_HEIGHT"] + TOLERANCE
        ):
            in_bounds_ok = False

        if expected_colors:
            expected_color = expected_colors[row // 2]
            actual_color = _normalize_color(rect.get("fill"))
            if actual_color != expected_color:
                colors_ok = False

    if coords_ok and len(rectangles) == expected_count:
        points += 12
    else:
        feedback.append("Bricks are not positioned in the expected grid layout.")

    if colors_ok and len(rectangles) == expected_count:
        points += 4
    else:
        feedback.append("Brick rows should use the expected color bands from COLORS.")

    if in_bounds_ok and len(rectangles) == expected_count:
        points += 4
    else:
        feedback.append("All bricks should be fully inside the canvas.")

    return points, 30, feedback


def _test_create_ball(namespace):
    if not callable(namespace.get("create_ball")):
        return 0, 10, ["create_ball(canvas) is missing or not callable."]

    missing = [name for name in ["CANVAS_WIDTH", "CANVAS_HEIGHT", "BALL_RADIUS"] if name not in namespace]
    if missing:
        return 0, 10, ["Missing constants needed to test the ball: " + ", ".join(missing)]

    canvas = MockCanvas(namespace["CANVAS_WIDTH"], namespace["CANVAS_HEIGHT"], "Breakout")
    try:
        ball_id = namespace["create_ball"](canvas)
    except Exception as e:
        return 0, 10, [f"create_ball(canvas) raised an error: {e}"]

    ovals = _get_shapes(canvas, "oval")
    if len(ovals) != 1:
        return 0, 10, [f"create_ball() should draw exactly one ball, but I found {len(ovals)} ovals."]

    obj_id, ball = ovals[0]
    expected_left = namespace["CANVAS_WIDTH"] / 2 - namespace["BALL_RADIUS"]
    expected_top = namespace["CANVAS_HEIGHT"] / 2 - namespace["BALL_RADIUS"]
    expected_right = expected_left + 2 * namespace["BALL_RADIUS"]
    expected_bottom = expected_top + 2 * namespace["BALL_RADIUS"]

    points = 0
    feedback = []

    if ball_id == obj_id:
        points += 2
    else:
        feedback.append("create_ball() should return the ball object it creates.")

    coords = ball["coords"]
    if (
        _is_close(coords[0], expected_left)
        and _is_close(coords[1], expected_top)
        and _is_close(coords[2], expected_right)
        and _is_close(coords[3], expected_bottom)
    ):
        points += 6
    else:
        feedback.append("The ball should start centered on the canvas with the correct radius.")

    if _normalize_color(ball.get("fill")) == "black":
        points += 2
    else:
        feedback.append("The ball should be drawn in black.")

    return points, 10, feedback


def _test_create_paddle(namespace):
    if not callable(namespace.get("create_paddle")):
        return 0, 10, ["create_paddle(canvas) is missing or not callable."]

    required = ["CANVAS_WIDTH", "CANVAS_HEIGHT", "PADDLE_WIDTH", "PADDLE_HEIGHT", "PADDLE_Y_OFFSET"]
    missing = [name for name in required if name not in namespace]
    if missing:
        return 0, 10, ["Missing constants needed to test the paddle: " + ", ".join(missing)]

    canvas = MockCanvas(namespace["CANVAS_WIDTH"], namespace["CANVAS_HEIGHT"], "Breakout")
    try:
        paddle_id = namespace["create_paddle"](canvas)
    except Exception as e:
        return 0, 10, [f"create_paddle(canvas) raised an error: {e}"]

    rectangles = _get_shapes(canvas, "rectangle")
    if len(rectangles) != 1:
        return 0, 10, [f"create_paddle() should draw exactly one paddle, but I found {len(rectangles)} rectangles."]

    obj_id, paddle = rectangles[0]
    expected_left = namespace["CANVAS_WIDTH"] / 2 - namespace["PADDLE_WIDTH"] / 2
    expected_top = namespace["CANVAS_HEIGHT"] - namespace["PADDLE_Y_OFFSET"] - namespace["PADDLE_HEIGHT"]
    expected_right = expected_left + namespace["PADDLE_WIDTH"]
    expected_bottom = expected_top + namespace["PADDLE_HEIGHT"]

    points = 0
    feedback = []

    if paddle_id == obj_id:
        points += 2
    else:
        feedback.append("create_paddle() should return the paddle object it creates.")

    coords = paddle["coords"]
    if (
        _is_close(coords[0], expected_left)
        and _is_close(coords[1], expected_top)
        and _is_close(coords[2], expected_right)
        and _is_close(coords[3], expected_bottom)
    ):
        points += 6
    else:
        feedback.append("The paddle should start centered near the bottom of the canvas.")

    if _normalize_color(paddle.get("fill")) == "black":
        points += 2
    else:
        feedback.append("The paddle should be drawn in black.")

    return points, 10, feedback


def _test_main_setup(namespace):
    main = namespace.get("main")
    if not callable(main):
        return 0, 25, ["main() is missing or not callable."]

    class StopMain(Exception):
        pass

    main_globals = main.__globals__
    original_create_bricks = main_globals.get("create_bricks")
    original_create_ball = main_globals.get("create_ball")
    original_create_paddle = main_globals.get("create_paddle")

    calls = {"create_bricks": 0, "create_ball": 0, "create_paddle": 0}

    def fake_create_bricks(canvas):
        calls["create_bricks"] += 1
        return set()

    def fake_create_ball(canvas):
        calls["create_ball"] += 1
        return "ball"

    def fake_create_paddle(canvas):
        calls["create_paddle"] += 1
        raise StopMain()

    main_globals["create_bricks"] = fake_create_bricks
    main_globals["create_ball"] = fake_create_ball
    main_globals["create_paddle"] = fake_create_paddle
    MockCanvas.instances = []

    try:
        main()
    except StopMain:
        pass
    except Exception as e:
        return 0, 25, [f"main() raised an unexpected error during setup: {e}"]
    finally:
        main_globals["create_bricks"] = original_create_bricks
        main_globals["create_ball"] = original_create_ball
        main_globals["create_paddle"] = original_create_paddle

    if not MockCanvas.instances:
        return 0, 25, ["main() should create a Canvas before starting the game."]

    canvas = MockCanvas.instances[0]
    points = 0
    feedback = []

    if (
        _is_close(_to_float(canvas.width), _to_float(namespace.get("CANVAS_WIDTH")))
        and _is_close(_to_float(canvas.height), _to_float(namespace.get("CANVAS_HEIGHT")))
    ):
        points += 10
    else:
        feedback.append("main() should create the canvas using CANVAS_WIDTH and CANVAS_HEIGHT.")

    if _normalize_color(canvas.background) == "white":
        points += 5
    else:
        feedback.append("main() should set the canvas background to white.")

    if calls == {"create_bricks": 1, "create_ball": 1, "create_paddle": 1}:
        points += 10
    else:
        feedback.append("main() should call create_bricks(), create_ball(), and create_paddle() once during setup.")

    return points, 25, feedback


def grade(student_file):
    tests = []

    try:
        tree = _parse_tree(student_file)
    except Exception as e:
        return 0, [f"Error parsing code: {e}"]

    tests.append(_test_static_api(tree))
    tests.append(_test_gameplay_signals(tree))

    try:
        namespace = _load_student_namespace(student_file)
    except TimeoutError as e:
        return 0, [str(e)]
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 0
        if code != 0:
            return 0, [f"Program exited early with code {code}."]
        namespace = {}
    except Exception as e:
        return 0, [f"Error loading student program: {e}"]

    tests.append(_test_create_bricks(namespace))
    tests.append(_test_create_ball(namespace))
    tests.append(_test_create_paddle(namespace))
    tests.append(_test_main_setup(namespace))

    score = 0
    feedback = []
    max_score = 0

    for points, maximum, messages in tests:
        score += points
        max_score += maximum
        feedback.extend(messages)

    if not feedback:
        feedback.append("Great job! Your Breakout program has the expected setup and core game structure.")

    if max_score <= 0:
        return 0, feedback

    final_score = round((score / max_score) * 100)
    return final_score, feedback
