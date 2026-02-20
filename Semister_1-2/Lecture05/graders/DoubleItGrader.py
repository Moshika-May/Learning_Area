
import sys
import subprocess
import ast

def run_test(student_file, valid_input, expected_sequence):
    try:
        proc = subprocess.run(
            [sys.executable, student_file],
            input=f"{valid_input}\n",
            text=True,
            capture_output=True,
            timeout=2
        )
    except subprocess.TimeoutExpired:
        return False, f"Timeout on input {valid_input}"

    if proc.returncode != 0:
        return False, f"Error on input {valid_input}: {proc.stderr}"
    
    # Parse output
    # Expected: "Enter a number: " then numbers.
    # We look for integers in the output.
    output_text = proc.stdout
    import re
    # Find all integers
    # Be careful not to capture the prompt "Enter a number: 2" -> 2 might be in the output if echoing?
    # Usually standard input is not echoed in captured stdout unless explicitly printed.
    
    # Let's extract numbers from lines.
    # Input prompt: "Enter a number: " -> usually no newline, so "2" comes after.
    # But if using input(), the prompt is in stdout.
    # So we might find valid_input in the output if we are not careful? No, input() prompt goes to stdout, but the user typed chars go to stdin.
    # If using terminal, echoed, but capture_output usually captures program write, not stdin echo.
    
    # Let's parse all numbers found in the output.
    # But filtering out the input validation? 
    # The prompt might contain numbers? "Enter a number: "
    
    # Use regex to find all integers in the output text
    # This handles "Enter a number: 4" case where 4 is on same line as prompt
    import re
    tokens = re.findall(r'-?\d+', output_text)
    found_numbers = [int(t) for t in tokens]
    
    # We might accidentally pick up numbers from prompt if prompt changes?
    # But "Enter a number: " is safe.
    # If found_numbers matches expected, good.
            
    if found_numbers != expected_sequence:
        return False, f"Input {valid_input}: Expected sequence {expected_sequence}, found {found_numbers}. Output:\n{output_text}"
        
    return True, "Success"

def grade(student_file):
    failures = []
    
    # Test assertions
    # 2 -> 4, 8, 16, 32, 64, 128
    ok, msg = run_test(student_file, 2, [4, 8, 16, 32, 64, 128])
    if not ok: failures.append(msg)
    
    # 50 -> 100
    ok, msg = run_test(student_file, 50, [100])
    if not ok: failures.append(msg)
    
    # 99 -> 198
    ok, msg = run_test(student_file, 99, [198])
    if not ok: failures.append(msg)
    
    # 100 -> [] (loop shouldn't run)
    ok, msg = run_test(student_file, 100, [])
    if not ok: failures.append(msg)

    # 101 -> [] (loop shouldn't run)
    ok, msg = run_test(student_file, 101, [])
    if not ok: failures.append(msg)
    
    # Static Checks
    try:
        with open(student_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        # Check variable 'curr_value'
        has_curr_value = False
        updates_curr_value = False
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == 'curr_value':
                has_curr_value = True
                if isinstance(node.ctx, ast.Store):
                    # Check if it's start or update
                    pass
        
        if not has_curr_value:
             failures.append("Variable 'curr_value' not found. Please use the variable name 'curr_value'.")

        # Check for while loop condition: curr_value < 100
        has_correct_loop = False
        for node in ast.walk(tree):
            if isinstance(node, ast.While):
                # Check condition
                # Should be Compare(left=Name(curr_value), ops=[Lt], comparators=[Num(100)])
                cond = node.test
                if isinstance(cond, ast.Compare):
                    if isinstance(cond.left, ast.Name) and cond.left.id == 'curr_value':
                        if len(cond.ops) == 1 and isinstance(cond.ops[0], ast.Lt):
                             if len(cond.comparators) == 1:
                                 comp = cond.comparators[0]
                                 val = None
                                 if isinstance(comp, ast.Constant): val = comp.value
                                 elif isinstance(comp, ast.Num): val = comp.n
                                 
                                 if val == 100:
                                     has_correct_loop = True
        
        if not has_correct_loop:
             failures.append("Did not find a while loop with condition 'while curr_value < 100:'.")

    except Exception as e:
        failures.append(f"Error parsing code: {e}")
        
    if failures:
        return 0, failures
        
    return 100, ["Great job! Your DoubleIt program works perfectly."]
