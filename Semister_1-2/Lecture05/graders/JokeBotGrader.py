
import sys
import subprocess
import ast

# Expected constants
EXPECTED_PROMPT = "What do you want? "
EXPECTED_JOKE = "Here is a joke for you! Karel is heading out to the grocery store. A programmer tells her: get a liter of milk, and if they have eggs, get 12. Karel returns with 13 liters of milk. The programmer asks why and Karel replies: 'because they had eggs'"
EXPECTED_SORRY = "Sorry I only tell jokes"

def run_test(student_file, user_input, expected_response_fragment):
    try:
        proc = subprocess.run(
            [sys.executable, student_file],
            input=f"{user_input}\n",
            text=True,
            capture_output=True,
            timeout=2
        )
    except subprocess.TimeoutExpired:
        return False, f"Timeout on input '{user_input}'"

    if proc.returncode != 0:
        return False, f"Error on input '{user_input}': {proc.stderr}"
    
    # Check output
    output = proc.stdout
    
    # We expect the prompt, then the response.
    # But since input() puts prompt in stdout, it might be there.
    # Crucially, we look for expectation in the output.
    
    if expected_response_fragment not in output:
        # For "Joke", it's long, so maybe we check substring or exact?
        # The prompt defines JOKE.
        return False, f"Input '{user_input}': Expected output to contain \n{repr(expected_response_fragment)}\nBut got:\n{output}"
        
    return True, "Success"

def grade(student_file):
    failures = []
    
    # 1. Test "Joke"
    ok, msg = run_test(student_file, "Joke", EXPECTED_JOKE)
    if not ok: failures.append(msg)
    
    # 2. Test "Hello" (Something else)
    ok, msg = run_test(student_file, "Hello", EXPECTED_SORRY)
    if not ok: failures.append(msg)

    # 3. Test "joke" (Case sensitive check implies this should trigger SORRY)
    ok, msg = run_test(student_file, "joke", EXPECTED_SORRY)
    if not ok: failures.append(msg)
    
    # Static Checks
    try:
        with open(student_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        # Check constants
        constants = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                # Check targets
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        # Get value
                        val = None
                        if isinstance(node.value, ast.Constant):
                            val = node.value.value
                        elif isinstance(node.value, ast.Str):
                            val = node.value.s
                        
                        constants[target.id] = val
        
        # Check PROMPT
        if 'PROMPT' not in constants:
            failures.append("Constant PROMPT not defined.")
        elif constants['PROMPT'] != EXPECTED_PROMPT:
            failures.append(f"Constant PROMPT does not match expected.\nExpected: {repr(EXPECTED_PROMPT)}\nActual:   {repr(constants['PROMPT'])}")

        # Check JOKE
        if 'JOKE' not in constants:
            failures.append("Constant JOKE not defined.")
        elif constants['JOKE'] != EXPECTED_JOKE:
            failures.append(f"Constant JOKE does not match expected.\nExpected: {repr(EXPECTED_JOKE)}\nActual:   {repr(constants['JOKE'])}")

        # Check SORRY
        if 'SORRY' not in constants:
            failures.append("Constant SORRY not defined.")
        elif constants['SORRY'] != EXPECTED_SORRY:
            failures.append(f"Constant SORRY does not match expected.\nExpected: {repr(EXPECTED_SORRY)}\nActual:   {repr(constants['SORRY'])}")
            
        # Check for if statement usage
        has_if = False
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                # Check condition roughly?
                # user_input == "Joke"
                has_if = True
        
        if not has_if:
            failures.append("Did not find an if statement.")

        # Check for hardcoded strings in input/print
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'input':
                    # Expect input(PROMPT)
                    if node.args:
                        arg = node.args[0]
                        # Check for string literal
                        if isinstance(arg, (ast.Constant, ast.Str)): 
                             # Python 3.8+ uses Constant for strings, older uses Str
                             # It's a string literal. Bad if it matches our expected prompt or generally if requirement is "Use Constant"
                             val = arg.value if isinstance(arg, ast.Constant) else arg.s
                             if val == EXPECTED_PROMPT:
                                 failures.append("Do not hardcode the prompt string in input(). Use the constant PROMPT.")

                if node.func.id == 'print':
                    # Expect print(JOKE) or print(SORRY)
                    if node.args:
                        arg = node.args[0]
                        if isinstance(arg, (ast.Constant, ast.Str)):
                             val = arg.value if isinstance(arg, ast.Constant) else arg.s
                             if val == EXPECTED_JOKE:
                                 failures.append("Do not hardcode the joke string in print(). Use the constant JOKE.")
                             if val == EXPECTED_SORRY:
                                 failures.append("Do not hardcode the sorry string in print(). Use the constant SORRY.")

    except Exception as e:
        failures.append(f"Error parsing code: {e}")

    if failures:
        return 0, failures
        
    return 100, ["Great job! Your JokeBot works perfectly."]
