"""Utilities for creating student files and running graders.

Provides:
- write_and_run_grader(problem_name: str, content: str) -> (score, feedback)
"""
from __future__ import annotations

import importlib
import os
from typing import List, Tuple


def write_student_file(base_name: str, content: str) -> str:
    """Write the given content to a file named <base_name>.py and return the filename.

    The base_name may include or omit the .py extension. Returns the relative path to the file.

    Ensures the file contains the canonical boilerplate exactly as:

    if __name__ == '__main__':
        run_karel_program()
    """
    import re

    if base_name.endswith('.py'):
        filename = base_name
    else:
        filename = f"{base_name}.py"

    canonical = "if __name__ == '__main__':\n    run_karel_program()\n"

    # If the provided content already contains the exact canonical boilerplate, use it as-is
    if canonical.strip() in content:
        final_content = content
    else:
        # If there's an existing __main__ block, replace it with the canonical block
        pattern = r"^if\s+__name__\s*==\s*['\"]__main__['\"]\s*:\s*(?:\n[ \t]+.*)*$"
        if re.search(pattern, content, flags=re.MULTILINE):
            final_content = re.sub(pattern, canonical.rstrip(), content, flags=re.MULTILINE)
            if not final_content.endswith("\n"):
                final_content += "\n"
        else:
            # Append the canonical block to the content, ensuring one blank line separation
            if not content.endswith("\n"):
                content = content + "\n"
            final_content = content + canonical

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_content)

    return filename


def write_and_run_grader(problem_name: str, content: str) -> Tuple[int, List[str]]:
    """Create a student file and run the corresponding grader.

    The problem_name (e.g. "StepUp") will create StepUp.py and attempt to run
    the corresponding grader (graders.StepUpGrader.grade on the created file).

    Returns (score, feedback_list) as returned by the grader. On error, returns
    (0, [<error message>]).
    """
    # Create the student file
    student_file = write_student_file(problem_name, content)

    # Resolve grader module name (e.g. StepUpGrader)
    grader_mod_name = f"{os.path.splitext(os.path.basename(student_file))[0]}Grader"

    # Try to import graders.<GraderName> then fallback to bare module name
    candidates = [f"graders.{grader_mod_name}", grader_mod_name]
    grader_mod = None
    last_exc = None
    for cand in candidates:
        try:
            grader_mod = importlib.import_module(cand)
            break
        except Exception as e:
            last_exc = e

    if grader_mod is None:
        return 0, [f"Could not import grader module for '{problem_name}': {last_exc}"]

    # Run the grader
    try:
        if not hasattr(grader_mod, 'grade'):
            return 0, [f"Grader module '{grader_mod.__name__}' has no 'grade' function."]
        result = grader_mod.grade(student_file)
        return result
    except Exception as e:
        return 0, [f"Grader execution error: {e}"]


if __name__ == '__main__':
    # Example usage (writes StepUp.py and runs the StepUp grader)
    code = """# This tells Python who Karel is
# Every Karel file has a line just like it
from karel.stanfordkarel import *

# this program executes in a special function called main
def main():
    move()
    pick_beeper()
    move()
    turn_left()
    move()
    turn_left()
    turn_left()
    turn_left()
    move()
    put_beeper()
    move()


# This is "boilerplate" code which launches your code
# when you hit the run button

main()
"""
    score, fb = write_and_run_grader('StepUp', code)
    print('Score:', score)
    print('\n'.join(fb))
