import sys
import subprocess
import ast
import re

def grade(student_file):
    """Grade Dice.py solutions.

    Expectations:
      - The program should prompt for number of sides.
      - It should simulate a roll and print the result.
      - Output should match the sample format.
      - Use good naming for variables.
    """
    failures = []

    # Test with sides = 10
    sides = 10
    input_str = f"{sides}\n"
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
            failures.append(f"Program produced stderr: {result.stderr}")
        if result.returncode != 0:
            failures.append(f"Program exited with code {result.returncode}")
        
        # Check output format
        expected_prompt = "How many sides does your dice have? "
        expected_roll_prefix = "Your roll is "
        if not actual_output.startswith(expected_prompt):
            failures.append("Program does not prompt correctly.")
        else:
            # Remove prompt
            remaining = actual_output[len(expected_prompt):].strip()
            if not remaining.startswith(expected_roll_prefix):
                failures.append("Program does not print roll correctly.")
            else:
                roll_str = remaining[len(expected_roll_prefix):].strip()
                try:
                    roll = int(roll_str)
                    if not (1 <= roll <= sides):
                        failures.append(f"Roll {roll} is not between 1 and {sides}.")
                except ValueError:
                    failures.append(f"Roll '{roll_str}' is not a valid integer.")
    except subprocess.TimeoutExpired:
        failures.append("Program timed out")
    except Exception as e:
        failures.append(f"Error running program: {e}")

    # Check for good naming and structure
    try:
        with open(student_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        # Check for random.randint usage with a variable for sides
        uses_variable_for_sides = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == 'random' and node.func.attr == 'randint':
                if len(node.args) == 2:
                    arg1 = node.args[0]
                    arg2 = node.args[1]
                    if isinstance(arg1, ast.Num) and arg1.n == 1 and isinstance(arg2, ast.Name):
                        uses_variable_for_sides = True
        if not uses_variable_for_sides:
            failures.append("Program does not use a variable for the number of sides in random.randint. It should be random.randint(1, variable_name).")
        
        # Check for input usage
        has_input = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'input':
                has_input = True
        if not has_input:
            failures.append("Program does not prompt for user input.")
        
        # Check variable names
        variables = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                variables.add(node.id)
        bad_var_names = {'a', 'b', 'c', 'x', 'y', 'z', 'i', 'j', 'k', 'temp', 'var', 'data', 't', 'r', 'roll', 'n', 'nn', 'nnn', 'aaa', 'bbb', 'xxx'}
        for var in variables:
            if var in bad_var_names or len(var) < 3:
                failures.append(f"Variable name '{var}' is not descriptive. Use meaningful names like 'sides' or 'dice_roll'.")
    except Exception as e:
        failures.append(f"Error parsing code: {e}")



    if failures:
        return 0, failures

    return 100, ["Correct: program prompts correctly, simulates roll, and uses good naming."]