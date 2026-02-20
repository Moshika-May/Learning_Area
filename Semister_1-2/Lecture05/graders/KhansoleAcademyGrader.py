import sys
import subprocess
import re
import ast

def run_interactive_test(student_file, give_correct=True):
    """
    Runs the student program, finds the addition question, inputs an answer 
    (correct or incorrect), and verifies the output.
    Returns (success, message, observed_nums)
    """
    proc = subprocess.Popen(
        [sys.executable, "-u", student_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )

    try:
        output_buffer = ""
        num1 = None
        num2 = None
        
        # Read until we find the question or run out of sensible output limit
        # A simple approach is to read line-by-line.
        # We need a timeout logic because readline() can block.
        # But subprocess.Popen doesn't have simple per-line timeout without threads/select.
        # Given the environment, let's use a simpler communicated-based approach if possible?
        # No, because we need to know the question BEFORE providing input.
        # So we stick to readline but we must rely on the student program printing a newline.
        # Most students use print() which adds newline.
        
        # We'll allow reading up to 20 lines to find the question.
        found_question = False
        for _ in range(20):
            line = proc.stdout.readline()
            if not line:
                break
            output_buffer += line
            
            # Look for pattern "What is X + Y?"
            # We allow some flexibility: "What is X + Y", "X + Y"
            m = re.search(r"What is (\d+)\s*\+\s*(\d+)", line, re.IGNORECASE)
            if not m:
                # Maybe they just printed "51 + 79?" without "What is"
                m = re.search(r"(\d+)\s*\+\s*(\d+)\?", line)
            
            if m:
                num1 = int(m.group(1))
                num2 = int(m.group(2))
                found_question = True
                break
        
        if not found_question:
            proc.kill()
            return False, "Could not find a line asking 'What is X + Y?'. Output so far:\n" + output_buffer, None

        if not (10 <= num1 <= 99 and 10 <= num2 <= 99):
            # We note this but continue testing correctness
            pass 

        expected_sum = num1 + num2
        user_answer = expected_sum if give_correct else (expected_sum + 13) # distinct incorrect ans
        
        # Send answer
        try:
            proc.stdin.write(f"{user_answer}\n")
            proc.stdin.flush()
        except BrokenPipeError:
            return False, "Program exited before accepting input.", (num1, num2)

        # Read rest of output
        # We can use communicate now to get the rest
        stdout_rest, stderr_rest = proc.communicate(timeout=2)
        full_output = output_buffer + stdout_rest
        
        if stderr_rest:
            return False, f"Program produced errors:\n{stderr_rest}", (num1, num2)

        if proc.returncode != 0:
            return False, f"Program exited with code {proc.returncode}", (num1, num2)

        # Check result
        if give_correct:
            # We want to match "Correct" or "correct" but NOT "Incorrect" or "incorrect"
            # Simplest way: check for "Correct!" or line that equals "Correct"
            # Or use regex word boundary.
            
            # Use regex to find "Correct" as a whole word, or just check that "Incorrect" is NOT present if "Correct" is present?
            # actually "Correct!" is what's expected.
            
            # If we just check checking:
            is_correct = False
            if "Correct!" in stdout_rest:
                is_correct = True
            elif re.search(r"\bCorrect\b", stdout_rest, re.IGNORECASE):
                 # Case insensitive whole word 'correct'
                 # But valid if it's not 'incorrect'
                 # "That is correct" -> matches. "Incorrect" -> does not match \bCorrect\b?
                 # \b matches boundary. "Incorrect": 't' is boundary? No.
                 # "Incorrect": I-n-c-o-r-r-e-c-t.
                 # \bCorrect\b matches " Correct " but not "Incorrect"
                 is_correct = True
            
            if is_correct:
                return True, "Success", (num1, num2)
            else:
                return False, f"Provided correct answer {user_answer} for {num1}+{num2}, but output did not contain 'Correct!'.\nOutput:\n{full_output}", (num1, num2)
        else:
            # Expect "Incorrect"
            if "Incorrect" in stdout_rest or "incorrect" in stdout_rest:
                # Optional: check if they print expected answer?
                # "The expected answer is 130"
                if str(expected_sum) not in stdout_rest:
                     return False, f"Your program correctly said Incorrect, but did not mention the expected answer {expected_sum}.\nOutput:\n{full_output}", (num1, num2)
                return True, "Success", (num1, num2)
            else:
                return False, f"Provided incorrect answer {user_answer} for {num1}+{num2}, but output did not contain 'Incorrect'.\nOutput:\n{full_output}", (num1, num2)

    except subprocess.TimeoutExpired:
        proc.kill()
        return False, "Program timed out.", (num1, num2)
    except Exception as e:
        proc.kill()
        return False, f"Test error: {e}", (num1, num2)


def grade(student_file):
    failures = []
    
    # Run Valid Test
    ok, msg, nums = run_interactive_test(student_file, give_correct=True)
    if not ok:
        failures.append(msg)
    else:
        # Check generated numbers range if captured
        if nums:
            n1, n2 = nums
            if not(10 <= n1 <= 99 and 10 <= n2 <= 99):
                failures.append(f"Generated numbers {n1} and {n2} are not both between 10 and 99.")

    # Run Incorrect Test
    ok, msg, nums = run_interactive_test(student_file, give_correct=False)
    if not ok:
        failures.append(msg)

    # Static Analysis
    try:
        with open(student_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        # Check imports
        imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
        if 'random' not in imports:
            failures.append("Program does not import 'random'.")
            
        # Check usage of random.randint
        correct_randint_calls = 0
        all_randint_args = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for random.randint
                if isinstance(node.func, ast.Attribute) and getattr(node.func.value, 'id', '') == 'random' and node.func.attr == 'randint':
                    # Check arguments
                    if len(node.args) == 2:
                        try:
                            # Try to get literal values
                            args = []
                            for arg in node.args:
                                if isinstance(arg, ast.Constant): # Python 3.8+
                                    args.append(arg.value)
                                elif isinstance(arg, ast.Num): # Python <3.8
                                    args.append(arg.n)
                            
                            if len(args) == 2:
                                arg_tuple = tuple(args)
                                all_randint_args.append(arg_tuple)
                                if args[0] == 10 and args[1] == 99:
                                    correct_randint_calls += 1
                        except:
                            pass
        
        if correct_randint_calls < 2:
             failures.append(f"Program should generate two random numbers between 10 and 99. Found {correct_randint_calls} calls to random.randint(10, 99). Detected calls: {all_randint_args}")

        # Check function names
        for node in ast.walk(tree):
             if isinstance(node, ast.FunctionDef):
                 name = node.name
                 if name != 'main':
                     if len(name) < 3 or name in {'func', 'function', 'test', 'do_it', 'stuff'}:
                         failures.append(f"Function name '{name}' is not descriptive. Use meaningful names.")

        # Check variable names
        variables = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                variables.add(node.id)
        
        # Filter commonly accepted loop variables if intended, but generally encourage descriptive names
        # 'i', 'j', 'k' are often okay for loops, but maybe we should be strict?
        # Let's add more non-descriptive names
        bad_var_names = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'n', 'm', 'x', 'y', 'z', 'temp', 'var', 'val', 'foo', 'bar'}
        for var in variables:
            # Check for bad list match
            if var in bad_var_names:
                 failures.append(f"Variable name '{var}' is not descriptive. Use meaningful names like 'num1' or 'answer'.")
            # Check length for non-loop variables (heuristic)
            elif len(var) == 1 and var not in {'i', 'j', 'k'}:
                 failures.append(f"Variable name '{var}' is too short. Use meaningful names.")

    except Exception as e:
        failures.append(f"Error analyzing code structure: {e}")

    if failures:
        return 0, failures
    
    return 100, ["Great job! Your Khansole Academy program works perfectly."]
