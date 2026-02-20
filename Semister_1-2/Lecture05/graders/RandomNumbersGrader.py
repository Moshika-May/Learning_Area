
import sys
import subprocess
import ast
import re

# Expected constants
EXPECTED_N_NUMBERS = 10
EXPECTED_MIN = 1
EXPECTED_MAX = 100

def run_test(student_file):
    try:
        proc = subprocess.run(
            [sys.executable, student_file],
            capture_output=True,
            text=True,
            timeout=2
        )
    except subprocess.TimeoutExpired:
        return False, "Program timed out.", []
        
    if proc.returncode != 0:
        return False, f"Program exited with code {proc.returncode}. Stderr: {proc.stderr}", []
        
    output = proc.stdout
    # Find all integers
    tokens = re.findall(r'-?\d+', output)
    numbers = []
    for t in tokens:
        try:
            numbers.append(int(t))
        except:
            pass
            
    return True, "Success", numbers

def grade(student_file):
    failures = []
    
    # 1. Dynamic Check
    # Run once
    ok, msg, numbers1 = run_test(student_file)
    if not ok:
        failures.append(msg)
    else:
        # Check count
        if len(numbers1) != EXPECTED_N_NUMBERS:
            failures.append(f"Expected {EXPECTED_N_NUMBERS} numbers, but found {len(numbers1)}. output: {numbers1}")
        
        # Check range
        out_of_range = [n for n in numbers1 if not (EXPECTED_MIN <= n <= EXPECTED_MAX)]
        if out_of_range:
            failures.append(f"Found numbers out of range [{EXPECTED_MIN}, {EXPECTED_MAX}]: {out_of_range}")
            
    # Run again to check randomness (heuristic)
    ok, msg, numbers2 = run_test(student_file)
    if ok and len(numbers1) == EXPECTED_N_NUMBERS and len(numbers2) == EXPECTED_N_NUMBERS:
        if numbers1 == numbers2:
             failures.append("Program output appears identical in two runs. Are numbers random?")
    
    # 2. Static Check
    try:
        with open(student_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        # Check Constants
        constants = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        val = None
                        if isinstance(node.value, ast.Constant):
                            val = node.value.value
                        elif isinstance(node.value, ast.Num):
                            val = node.value.n
                        constants[target.id] = val
        
        if 'N_NUMBERS' not in constants:
            failures.append("Constant N_NUMBERS not defined.")
        elif constants['N_NUMBERS'] != EXPECTED_N_NUMBERS:
            failures.append(f"N_NUMBERS should be {EXPECTED_N_NUMBERS}, found {constants['N_NUMBERS']}.")

        if 'MIN_VALUE' not in constants:
            failures.append("Constant MIN_VALUE not defined.")
        elif constants['MIN_VALUE'] != EXPECTED_MIN:
            failures.append(f"MIN_VALUE should be {EXPECTED_MIN}, found {constants['MIN_VALUE']}.")

        if 'MAX_VALUE' not in constants:
            failures.append("Constant MAX_VALUE not defined.")
        elif constants['MAX_VALUE'] != EXPECTED_MAX:
             failures.append(f"MAX_VALUE should be {EXPECTED_MAX}, found {constants['MAX_VALUE']}.")
             
        # Check usage in random.randint(MIN_VALUE, MAX_VALUE)
        has_correct_call = False
        randint_calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and getattr(node.func.value, 'id', '') == 'random' and node.func.attr == 'randint':
                    # Check args
                    if len(node.args) == 2:
                        arg1 = node.args[0]
                        arg2 = node.args[1]
                        
                        args_repr = []
                        is_correct = True
                        
                        # Check arg1 is Name(MIN_VALUE)
                        if isinstance(arg1, ast.Name):
                            args_repr.append(arg1.id)
                            if arg1.id != 'MIN_VALUE': is_correct = False
                        else:
                            args_repr.append("Literal/Expr")
                            is_correct = False
                            
                        # Check arg2 is Name(MAX_VALUE)
                        if isinstance(arg2, ast.Name):
                            args_repr.append(arg2.id)
                            if arg2.id != 'MAX_VALUE': is_correct = False
                        else:
                            args_repr.append("Literal/Expr")
                            is_correct = False
                            
                        randint_calls.append(tuple(args_repr))
                        if is_correct:
                            has_correct_call = True
        
        if not randint_calls:
            failures.append("Did not find any call to random.randint().")
        elif not has_correct_call:
            failures.append(f"Expected random.randint(MIN_VALUE, MAX_VALUE). Found calls with arguments: {randint_calls}")

        # Check loop range usage? range(N_NUMBERS)
        has_correct_loop = False
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                # check iter
                if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                    if node.iter.args:
                        arg0 = node.iter.args[0]
                        if isinstance(arg0, ast.Name) and arg0.id == 'N_NUMBERS':
                            has_correct_loop = True
        
        if not has_correct_loop:
            failures.append("Did not find a loop using range(N_NUMBERS).")

    except Exception as e:
        failures.append(f"Error analyzing code: {e}")
        
    if failures:
        return 0, failures

    return 100, ["Great job! Your RandomNumbers program works perfectly."]
