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
            world_file = "worlds/StoneMason.w"

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
    """Grade StoneMason solutions.

    Expectations (for every world matching worlds/StoneMason*.w):
      - After execution, beepers are present only at avenues 1, 5, 9, 13 on streets 1 through 5, each with exactly one beeper.
      - No beepers exist elsewhere.
      - Karel ends at (num_avenues, 1) facing east.
    """
    global CAPTURED_WORLD

    world_files = sorted(glob.glob("worlds/StoneMason*.w"))
    if not world_files:
        world_files = ["worlds/StoneMason.w"]

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

        # Expected beeper positions: avenues 1,5,9,13 on streets 1 to 5
        expected_avenues = [1, 5, 9, 13]
        expected_positions = []
        for a in expected_avenues:
            if a > width:
                continue
            for s in range(1, 6):  # streets 1 to 5
                if s <= height:
                    expected_positions.append((a, s))

        beepers = world.beepers
        wrong_counts = []
        extra_beepers = []

        # Check expected positions have exactly 1
        for pos in expected_positions:
            cnt = beepers.get(pos, 0)
            if cnt != 1:
                wrong_counts.append((pos, cnt))

        # Check no beepers elsewhere
        for (a, s), cnt in beepers.items():
            if cnt > 0 and (a, s) not in expected_positions:
                extra_beepers.append(((a, s), cnt))

        if wrong_counts:
            failures.append(f"{os.path.basename(wf)}: Expected exactly 1 beeper at each of {expected_positions}, found mismatches: {wrong_counts}.")
            continue

        if extra_beepers:
            failures.append(f"{os.path.basename(wf)}: Unexpected beepers elsewhere: {extra_beepers}.")
            continue

        # Check Karel final position and orientation
        k = getattr(world, 'karel', None)
        if k is None:
            failures.append(f"{os.path.basename(wf)}: Could not find Karel instance to check final position and orientation.")
            continue

        expected_pos = (width, 1)
        if (k.avenue, k.street) != expected_pos:
            failures.append(f"{os.path.basename(wf)}: Karel final position expected {expected_pos}, found ({k.avenue},{k.street}).")
            continue

        if not k.facing_east():
            failures.append(f"{os.path.basename(wf)}: Karel must be facing east at the end.")
            continue

    if failures:
        return 0, failures

    return 100, ["Correct: columns built with beepers at avenues 1, 5, 9, 13 (5 rows high) and Karel at the eastern wall facing east for all StoneMason worlds"]