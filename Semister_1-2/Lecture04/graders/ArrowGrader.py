import runpy
import io
import contextlib
import ast
from collections import Counter

def grade(student_file):
    """Grade arrow.py solutions.

    Expectations:
      - The program should produce the correct arrow output.
      - The code should use functions to capture structure and repetition (at least one user-defined function besides main).
    """
    failures = []

    # Expected output
    expected_output = """ /\\
/  \\

 /\\
/  \\

 ||
 ||
 /\\
/  \\

\\  /
 \\/
 /\\
/  \\

"""

    # Capture output
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            runpy.run_path(student_file, run_name="__main__")
    except Exception as e:
        failures.append(f"Runtime error: {e}")
        return 0, failures

    actual_output = output_buffer.getvalue()

    if actual_output != expected_output:
        failures.append("Output does not match expected arrow pattern.")
        failures.append(f"Expected:\n{repr(expected_output)}")
        failures.append(f"Actual:\n{repr(actual_output)}")

    # Check for functions
    try:
        with open(student_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if 'main' in functions:
            functions.remove('main')
        if not functions:
            failures.append("No user-defined functions found. Expected functions to capture structure and repetition.")
        
        # Check for good function naming
        bad_names = {'f', 'func', 'function', 'a', 'b', 'c', 'x', 'y', 'z', 'foo', 'bar', 'test', 'fn'}
        for name in functions:
            if name in bad_names or len(name) < 3:
                failures.append(f"Function name '{name}' is not descriptive. Use meaningful names like 'triangle' or 'stem'.")
        
        # Check for redundancy in print statements
        print_info = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
                for arg in node.args:
                    if isinstance(arg, ast.Str):
                        print_info.append((arg.s, node.lineno))
        from collections import defaultdict
        line_counts = defaultdict(list)
        for s, lineno in print_info:
            line_counts[s].append(lineno)
        redundant = {s: lines for s, lines in line_counts.items() if len(lines) > 2}
        if redundant:
            for s, lines in redundant.items():
                lines_str = ', '.join(map(str, lines))
                failures.append(f"Line {lines_str}: You must not print the {s!r} lines more than once.")
    except Exception as e:
        failures.append(f"Error parsing code: {e}")

    if failures:
        return 0, failures

    return 100, ["Correct: arrow output matches and functions are used for structure."]