import sys
import runpy
import io
import contextlib
import ast
from collections import Counter

def grade(student_file):
    """Grade Receipt.py solutions.

    Expectations:
      - The program should produce the correct receipt output.
      - Use variables and expressions to avoid repeating calculations.
      - Use good naming for variables.
    """
    failures = []

    # Expected output
    expected_output = """Subtotal:
108
Tax:
8.64
Tip:
16.2
Total:
132.84
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
        failures.append("Output does not match expected receipt.")
        failures.append(f"Expected:\n{repr(expected_output)}")
        failures.append(f"Actual:\n{repr(actual_output)}")

    # Check for avoiding repeated calculations
    try:
        with open(student_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        # Check that '38 + 40 + 30' appears at most once
        if source.count('38 + 40 + 30') > 1:
            failures.append("Repeated calculation: '38 + 40 + 30' appears more than once. Use a variable for subtotal.")
        
        # Check for variable assignments
        has_subtotal_var = False
        variables = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.add(target.id)
                        if target.id.lower() in ['subtotal', 'total', 'sum', 'amount']:
                            has_subtotal_var = True
        if not has_subtotal_var:
            failures.append("No variable found for subtotal. Define a variable like 'subtotal' to store 38 + 40 + 30.")
        
        # Check variable names
        bad_var_names = {'a', 'b', 'c', 'x', 'y', 'z', 'i', 'j', 'k', 'temp', 'var', 'data', 't'}
        for var in variables:
            if var in bad_var_names or len(var) < 3:
                failures.append(f"Variable name '{var}' is not descriptive. Use meaningful names like 'subtotal' or 'tax'.")
    except Exception as e:
        failures.append(f"Error parsing code: {e}")

    if failures:
        return 0, failures

    return 100, ["Correct: receipt output matches and calculations are not repeated using variables."]