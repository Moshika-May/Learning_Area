import os
import runpy
import signal
import sys
import types

TIMEOUT_SECONDS = 2


TEST_CASES = [
    {
        "name": "4x3 image",
        "pixels": [
            [(10, 20, 30), (40, 50, 60), (70, 80, 90), (100, 110, 120)],
            [(130, 140, 150), (160, 170, 180), (190, 200, 210), (220, 230, 240)],
            [(5, 15, 25), (35, 45, 55), (65, 75, 85), (95, 105, 115)],
        ],
    },
    {
        "name": "5x2 image",
        "pixels": [
            [(1, 2, 3), (11, 12, 13), (21, 22, 23), (31, 32, 33), (41, 42, 43)],
            [(51, 52, 53), (61, 62, 63), (71, 72, 73), (81, 82, 83), (91, 92, 93)],
        ],
    },
]


class TimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError("Program timed out.")


def _clamp(value):
    value = int(value)
    if value < 0:
        return 0
    if value > 255:
        return 255
    return value


class MockPixel:
    def __init__(self, image, x, y):
        self.image = image
        self._x = x
        self._y = y

    @property
    def red(self):
        return self.image.pixels[self._y][self._x][0]

    @red.setter
    def red(self, value):
        _, green, blue = self.image.pixels[self._y][self._x]
        self.image.pixels[self._y][self._x] = (_clamp(value), green, blue)

    @property
    def green(self):
        return self.image.pixels[self._y][self._x][1]

    @green.setter
    def green(self, value):
        red, _, blue = self.image.pixels[self._y][self._x]
        self.image.pixels[self._y][self._x] = (red, _clamp(value), blue)

    @property
    def blue(self):
        return self.image.pixels[self._y][self._x][2]

    @blue.setter
    def blue(self, value):
        red, green, _ = self.image.pixels[self._y][self._x]
        self.image.pixels[self._y][self._x] = (red, green, _clamp(value))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class MockSimpleImage:
    current_source_pixels = None
    shown_images = []
    loaded_filenames = []

    def __init__(self, filename, width=0, height=0, back_color=None):
        self.curr_x = 0
        self.curr_y = 0
        if filename:
            if MockSimpleImage.current_source_pixels is None:
                raise Exception("No source image configured for test case.")
            self._filename = filename
            MockSimpleImage.loaded_filenames.append(filename)
            self.pixels = copy_pixels(MockSimpleImage.current_source_pixels)
        else:
            if width <= 0 or height <= 0:
                raise Exception("Creating blank image requires width and height.")
            self._filename = ""
            self.pixels = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
        self._height = len(self.pixels)
        self._width = len(self.pixels[0]) if self._height else 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_x < self.width and self.curr_y < self.height:
            pixel = MockPixel(self, self.curr_x, self.curr_y)
            self.curr_x += 1
            if self.curr_x == self.width:
                self.curr_x = 0
                self.curr_y += 1
            return pixel
        self.curr_x = 0
        self.curr_y = 0
        raise StopIteration()

    @classmethod
    def blank(cls, width, height, back_color=None):
        return cls("", width=width, height=height, back_color=back_color)

    @classmethod
    def file(cls, filename):
        return cls(filename)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def get_pixel(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise Exception("get_pixel bad coordinate")
        return MockPixel(self, x, y)

    def set_pixel(self, x, y, pixel):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise Exception("set_pixel bad coordinate")
        self.pixels[y][x] = (pixel.red, pixel.green, pixel.blue)

    def set_rgb(self, x, y, red, green, blue):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise Exception("set_rgb bad coordinate")
        self.pixels[y][x] = (_clamp(red), _clamp(green), _clamp(blue))

    def show(self):
        MockSimpleImage.shown_images.append(copy_pixels(self.pixels))


def copy_pixels(pixels):
    return [[tuple(pixel) for pixel in row] for row in pixels]


def compare_images(expected, actual):
    if len(expected) != len(actual):
        return False, f"Expected image height {len(expected)}, but got {len(actual)}."
    if expected and actual and len(expected[0]) != len(actual[0]):
        return False, f"Expected image width {len(expected[0])}, but got {len(actual[0])}."

    for y, (expected_row, actual_row) in enumerate(zip(expected, actual)):
        if len(expected_row) != len(actual_row):
            return False, f"Row {y} has width {len(actual_row)} instead of {len(expected_row)}."
        for x, (expected_pixel, actual_pixel) in enumerate(zip(expected_row, actual_row)):
            if tuple(expected_pixel) != tuple(actual_pixel):
                return (
                    False,
                    "Pixel mismatch at "
                    f"({x}, {y}): expected {format_pixel(expected_pixel)}, "
                    f"got {format_pixel(actual_pixel)}.",
                )
    return True, "Success"


def format_pixel(pixel):
    return f"({pixel[0]}, {pixel[1]}, {pixel[2]})"


def loaded_stanford_image():
    return any(os.path.basename(str(filename)) == "stanford.jpg" for filename in MockSimpleImage.loaded_filenames)


def run_student(student_file, pixels):
    fake_simpleimage = types.ModuleType("simpleimage")
    fake_simpleimage.SimpleImage = MockSimpleImage

    old_simpleimage = sys.modules.get("simpleimage")
    MockSimpleImage.current_source_pixels = copy_pixels(pixels)
    MockSimpleImage.shown_images = []
    MockSimpleImage.loaded_filenames = []

    sys.modules["simpleimage"] = fake_simpleimage

    has_alarm = hasattr(signal, "SIGALRM")
    if has_alarm:
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(TIMEOUT_SECONDS)

    try:
        runpy.run_path(student_file, run_name="__main__")
    finally:
        if has_alarm:
            signal.alarm(0)
        if old_simpleimage is not None:
            sys.modules["simpleimage"] = old_simpleimage
        else:
            sys.modules.pop("simpleimage", None)


def grade_image_transform(student_file, transform, success_message, output_name):
    for case in TEST_CASES:
        try:
            run_student(student_file, case["pixels"])
        except TimeoutError as e:
            return 0, [str(e)]
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 0
            if code != 0:
                return 0, [f"Program exited early with code {code}."]
        except Exception as e:
            return 0, [f"Error running program on {case['name']}: {e}"]

        if not MockSimpleImage.loaded_filenames:
            return 0, ["Program did not load an image using SimpleImage(...)."]

        if not loaded_stanford_image():
            return 0, ["Program should load stanford.jpg."]

        if not MockSimpleImage.shown_images:
            return 0, [f"Program did not call show() on the {output_name}."]

        actual = MockSimpleImage.shown_images[-1]
        expected = transform(case["pixels"])
        ok, msg = compare_images(expected, actual)
        if not ok:
            return 0, [f"{case['name']}: {msg}"]

    return 100, [success_message]
