import sys
import runpy

CAPTURED_WORLD = None

import karel.KarelWorld as KW
import karel.stanfordkarel
from karel.Karel import Karel
import os
import glob


class CapturingKarelWorld(KW.KarelWorld):
    def __init__(self, *args, **kwargs):
        global CAPTURED_WORLD
        super().__init__(*args, **kwargs)
        CAPTURED_WORLD = self


# Patch the class where stanfordkarel imports it
KW.KarelWorld = CapturingKarelWorld


def headless_run_karel_program(world_file=None):
    # Determine world file
    student_file = sys.argv[0]
    base = os.path.basename(student_file)
    name = os.path.splitext(base)[0]

    if world_file is None:
        possible = f"worlds/{name}.w"
        if os.path.exists(possible):
            world_file = possible
        else:
            world_file = "worlds/FillAll.w"

    f = open(world_file, "r")
    world = KW.KarelWorld(f)
    karel = Karel(world)

    # Attach karel instance to world so grader can inspect final position
    world.karel = karel

    # Inject karel methods into student's __main__ namespace
    student_mod = sys.modules['__main__']

    student_mod.turn_left = karel.turn_left
    student_mod.move = karel.move
    student_mod.pick_beeper = karel.pick_beeper
    student_mod.put_beeper = karel.put_beeper
    student_mod.facing_north = karel.facing_north
    student_mod.facing_south = karel.facing_south
    student_mod.facing_east = karel.facing_east
    student_mod.facing_west = karel.facing_west
    student_mod.not_facing_north = karel.not_facing_north
    student_mod.not_facing_south = karel.not_facing_south
    student_mod.not_facing_east = karel.not_facing_east
    student_mod.not_facing_west = karel.not_facing_west
    student_mod.front_is_clear = karel.front_is_clear
    student_mod.beepers_present = karel.beepers_present
    student_mod.no_beepers_present = karel.no_beepers_present
    student_mod.beepers_in_bag = karel.beepers_in_bag
    student_mod.no_beepers_in_bag = karel.no_beepers_in_bag
    student_mod.front_is_blocked = karel.front_is_blocked
    student_mod.left_is_clear = karel.left_is_clear
    student_mod.left_is_blocked = karel.left_is_blocked
    student_mod.right_is_clear = karel.right_is_clear
    student_mod.right_is_blocked = karel.right_is_blocked
    student_mod.paint_corner = karel.paint_corner
    student_mod.corner_color_is = karel.corner_color_is

    if hasattr(student_mod, 'main'):
        student_mod.main()


def grade(student_file):
    """Grade FillAll solutions.

    Expectations (for every world matching worlds/FillAll*.w):
      - After execution, every corner in the world (1..num_avenues, 1..num_streets) has exactly one beeper.
      - No extra beepers exist elsewhere (total beepers == num_avenues * num_streets).
      - Karel ends at (num_avenues, num_streets) facing east.
    """
    global CAPTURED_WORLD

    world_files = sorted(glob.glob("worlds/FillAll*.w"))
    if not world_files:
        world_files = ["worlds/FillAll.w"]

    failures = []

    for wf in world_files:
        CAPTURED_WORLD = None

        # Patch runner to use this specific world file
        karel.stanfordkarel.run_karel_program = (lambda world_file=wf: headless_run_karel_program(world_file=world_file))

        sys.argv = [student_file]

        try:
            runpy.run_path(student_file, run_name="__main__")
        except Exception as e:
            failures.append(f"{os.path.basename(wf)}: Runtime error: {e}")
            continue

        if CAPTURED_WORLD is None:
            failures.append(f"{os.path.basename(wf)}: Karel world was not created")
            continue

        world = CAPTURED_WORLD
        width = world.num_avenues
        height = world.num_streets

        # Verify beepers on all corners
        beepers = world.beepers
        wrong_counts = []
        for a in range(1, width + 1):
            for s in range(1, height + 1):
                cnt = beepers.get((a, s), 0)
                if cnt != 1:
                    wrong_counts.append(((a, s), cnt))
        total_beepers = sum(count for count in beepers.values() if count > 0)

        if wrong_counts:
            failures.append(f"{os.path.basename(wf)}: Expected exactly 1 beeper at each corner, found mismatches: {wrong_counts}.")
            continue

        if total_beepers != width * height:
            failures.append(f"{os.path.basename(wf)}: Expected total beepers == {width * height}, found {total_beepers}.")
            continue

        # Check Karel final position and orientation
        k = getattr(world, 'karel', None)
        if k is None:
            failures.append(f"{os.path.basename(wf)}: Could not find Karel instance to check final position and orientation.")
            continue

        expected_pos = (width, height)
        if (k.avenue, k.street) != expected_pos:
            failures.append(f"{os.path.basename(wf)}: Karel final position expected {expected_pos}, found ({k.avenue},{k.street}).")
            continue

        if not k.facing_east():
            failures.append(f"{os.path.basename(wf)}: Karel must be facing east at the end.")
            continue

    if failures:
        return 0, failures

    return 100, ["Correct: entire world filled with one beeper per corner and Karel at the top-right corner facing east for all FillAll worlds"]