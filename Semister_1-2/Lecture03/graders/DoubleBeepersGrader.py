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
            world_file = "worlds/DoubleBeepers.w"

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
    """Grade DoubleBeepers solutions.

    Expectations (for every world matching worlds/DoubleBeepers*.w):
      - After execution, every corner that initially had beepers should now have exactly double the number of beepers.
      - No beepers should exist on corners that initially had none.
      - Total beepers should be double the initial total.
    """
    global CAPTURED_WORLD

    world_files = sorted(glob.glob("worlds/DoubleBeepers*.w"))
    if not world_files:
        world_files = ["worlds/DoubleBeepers.w"]

    failures = []

    for wf in world_files:
        CAPTURED_WORLD = None

        # Load initial world to get initial beeper state
        f = open(wf, "r")
        initial_world = KW.KarelWorld(f)
        initial_beepers = dict(initial_world.beepers)  # copy

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
        final_beepers = world.beepers

        # Check that each initial beeper location has exactly double
        for pos, count in initial_beepers.items():
            expected = count * 2
            actual = final_beepers.get(pos, 0)
            if actual != expected:
                failures.append(f"{os.path.basename(wf)}: At {pos}, expected {expected} beepers, found {actual}.")
                break
        else:
            # Check no extra beepers
            for pos, count in final_beepers.items():
                if pos not in initial_beepers and count > 0:
                    failures.append(f"{os.path.basename(wf)}: Unexpected beepers at {pos}: {count}.")
                    break
            else:
                # Check total beepers
                initial_total = sum(initial_beepers.values())
                final_total = sum(final_beepers.values())
                if final_total != initial_total * 2:
                    failures.append(f"{os.path.basename(wf)}: Total beepers expected {initial_total * 2}, found {final_total}.")
                    continue

    if failures:
        return 0, failures

    return 100, ["Correct: all initial beeper piles doubled in place for all DoubleBeepers worlds"]