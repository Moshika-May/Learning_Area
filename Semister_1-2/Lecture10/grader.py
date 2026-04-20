import importlib
import os
import sys
import pkgutil


def discover_problems():
    """Discover grader modules in the `graders` package and return problem names."""
    try:
        import graders
        problems = []
        for _, modname, _ in pkgutil.iter_modules(graders.__path__):
            if modname.endswith('Grader'):
                problems.append(modname[:-6])  # strip 'Grader'
        if problems:
            return sorted(problems)
    except Exception:
        pass
    # Fallback for backward compatibility
    return ['StepUp']


problems = discover_problems()


def import_grader(name):
    """Try to import grader by name, preferring the `graders` package and falling back to `karel`.

    Attempts the following candidates (in order):
    - name
    - graders.name
    - karel.name
    """
    candidates = [name, f'graders.{name}', f'karel.{name}']
    last_exc = None
    for candidate in candidates:
        try:
            return importlib.import_module(candidate)
        except Exception as e:
            last_exc = e
    raise ImportError(f"Could not import grader '{name}': {last_exc}")


def choose_problem(problems_list):
    """Show available problems and return the chosen problem name (e.g. 'StepUp')."""
    print("Available problems:")
    for idx, p in enumerate(problems_list, start=1):
        print(f" {idx}. {p}")

    while True:
        choice = input("Enter problem number: ").strip()
        if not choice:
            print("Please enter a number.")
            continue
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue
        n = int(choice)
        if 1 <= n <= len(problems_list):
            return problems_list[n - 1]
        print(f"Number must be between 1 and {len(problems_list)}")

# Keep a backward-compatible name for callers that expect choose_grader
choose_grader = choose_problem


def choose_student_file(default='source.py'):
    prompt = f"Enter student file to grade (default: {default}): "
    while True:
        path = input(prompt).strip()
        if not path:
            path = default
        if os.path.exists(path):
            return path
        print(f"File '{path}' does not exist; please try again.")


def run_grader_module(grader_module, student_file):
    if not hasattr(grader_module, 'grade'):
        print(f"Module {grader_module.__name__} has no 'grade' function.")
        return
    try:
        score, feedback = grader_module.grade(student_file)
    except Exception as e:
        print(f"Grader raised an exception: {e}")
        return

    print('\nResult:')
    print(f"Score: {score}")
    print("Feedback:")
    for line in feedback:
        print(f" - {line}")


if __name__ == '__main__':
    selected_problem = choose_problem(problems)

    # Derive grader module name and default student file from problem name
    grader_name = f"{selected_problem}Grader"
    try:
        mod = import_grader(grader_name)
    except ImportError as e:
        print(e)
        sys.exit(1)

    default_student = f"{selected_problem}.py"
    student_file = choose_student_file(default=default_student)
    run_grader_module(mod, student_file)
