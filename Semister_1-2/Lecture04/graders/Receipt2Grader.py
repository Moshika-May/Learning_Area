import sys
import subprocess
import ast
from collections import Counter

def grade(student_file):
    """Grade Receipt2.py solutions.

    Expectations:
      - The program should be interactive, prompting for meal cost.
      - It should compute tax (8%), tip (15%), and total correctly.
      - Output should match the sample format.
      - Use good naming for variables.
    """
    failures = []

    # Test cases: (input_cost, expected_output)
    test_cases = [
        ("50", "What was the meal cost? $Subtotal: 50\nTax: 4.0\nTip: 7.5\nTotal: 61.5\n"),
        ("125", "What was the meal cost? $Subtotal: 125\nTax: 10.0\nTip: 18.75\nTotal: 153.75\n"),
    ]

    for input_cost, expected in test_cases:
        input_str = f"{input_cost}\n"
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
                failures.append(f"For input ${input_cost}: Program produced stderr: {result.stderr}")
            if result.returncode != 0:
                failures.append(f"For input ${input_cost}: Program exited with code {result.returncode}")
            if actual_output != expected:
                failures.append(f"For input ${input_cost}: Output does not match expected.")
                failures.append(f"Expected:\n{repr(expected)}")
                failures.append(f"Actual:\n{repr(actual_output)}")
        except subprocess.TimeoutExpired:
            failures.append(f"For input ${input_cost}: Program timed out")
        except Exception as e:
            failures.append(f"For input ${input_cost}: Error running program: {e}")

    # Check for good naming
    try:
        with open(student_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        # Check variable names
        variables = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                variables.add(node.id)
        bad_var_names = {'a', 'b', 'c', 'x', 'y', 'z', 'i', 'j', 'k', 'temp', 'var', 'data', 't', 'cost'}
        for var in variables:
            if var in bad_var_names or len(var) < 3:
                failures.append(f"Variable name '{var}' is not descriptive. Use meaningful names like 'subtotal' or 'meal_cost'.")
        
        # Check for input usage
        has_input = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'input':
                has_input = True
                break
        if not has_input:
            failures.append("Program does not prompt for user input. Use input() to read the meal cost.")
    except Exception as e:
        failures.append(f"Error parsing code: {e}")

    if failures:
        return 0, failures

    return 100, ["Correct: program is interactive, computes correctly, and uses good naming."]