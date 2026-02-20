import sys
import subprocess
import ast
from collections import Counter

def grade(student_file):
    """Grade inches_to_centimeters.py solutions.

    Expectations:
      - The program should be interactive, prompting for feet and inches.
      - It should convert correctly to centimeters.
      - Output should match the sample format.
      - Use good naming for variables and functions.
    """
    failures = []

    # Test cases: (feet, inches, expected_output)
    test_cases = [
        (0, 0, "This program converts feet and inches to centimeters.\nEnter number of feet: Enter number of inches: 0 ft 0 in = 0.0 cm\n"),
        (1, 0, "This program converts feet and inches to centimeters.\nEnter number of feet: Enter number of inches: 1 ft 0 in = 30.48 cm\n"),
        (0, 1, "This program converts feet and inches to centimeters.\nEnter number of feet: Enter number of inches: 0 ft 1 in = 2.54 cm\n"),
        (5, 11, "This program converts feet and inches to centimeters.\nEnter number of feet: Enter number of inches: 5 ft 11 in = 180.34 cm\n"),
    ]

    for feet, inches, expected in test_cases:
        input_str = f"{feet}\n{inches}\n"
        try:
            result = subprocess.run(
                [sys.executable, student_file],
                input=input_str,
                text=True,
                capture_output=True,
                timeout=10
            )
            actual_output = result.stdout
            if result.stderr:
                failures.append(f"For input {feet} ft {inches} in: Program produced stderr: {result.stderr}")
            if result.returncode != 0:
                failures.append(f"For input {feet} ft {inches} in: Program exited with code {result.returncode}")
            if actual_output != expected:
                failures.append(f"For input {feet} ft {inches} in: Output does not match expected.")
                failures.append(f"Expected:\n{repr(expected)}")
                failures.append(f"Actual:\n{repr(actual_output)}")
        except subprocess.TimeoutExpired:
            failures.append(f"For input {feet} ft {inches} in: Program timed out")
        except Exception as e:
            failures.append(f"For input {feet} ft {inches} in: Error running program: {e}")

    # Check for good naming
    try:
        with open(student_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if 'main' in functions:
            functions.remove('main')
        if not functions:
            # No functions besides main is ok for this simple program
            pass
        
        # Check function names
        bad_names = {'f', 'func', 'function', 'a', 'b', 'c', 'x', 'y', 'z', 'foo', 'bar', 'test', 'fn'}
        for name in functions:
            if name in bad_names or len(name) < 3:
                failures.append(f"Function name '{name}' is not descriptive. Use meaningful names.")
        
        # Check variable names
        variables = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                variables.add(node.id)
        bad_var_names = {'a', 'b', 'c', 'x', 'y', 'z', 'i', 'j', 'k', 'temp', 'var', 'data'}
        for var in variables:
            if var in bad_var_names or len(var) < 3:
                failures.append(f"Variable name '{var}' is not descriptive. Use meaningful names like 'feet' or 'inches'.")
    except Exception as e:
        failures.append(f"Error parsing code: {e}")

    if failures:
        return 0, failures

    return 100, ["Correct: program works correctly and uses good naming."]