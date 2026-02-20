import sys
import runpy

CAPTURED_WORLD = None

import karel.KarelWorld as KW
import karel.stanfordkarel
from karel.Karel import Karel
import os


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
            world_file = "worlds/KarelsHome.w"

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
    """Grade KarelsHome solutions.

    Expectations:
      - The single beeper at (5,3) is picked up (no beepers remain in the world).
      - Karel ends at (2,4) facing east.
    """
    global CAPTURED_WORLD
    CAPTURED_WORLD = None

    # Patch runner
    karel.stanfordkarel.run_karel_program = headless_run_karel_program

    sys.argv = [student_file]

    try:
        runpy.run_path(student_file, run_name="__main__")
    except Exception as e:
        return 0, [f"Runtime error: {e}"]

    if CAPTURED_WORLD is None:
        return 0, ["Karel world was not created"]

    world = CAPTURED_WORLD
    feedback = []
    score = 100

    # Check beeper at (5,3) was picked up (no beepers remain)
    beepers = world.beepers
    beeper_count_at_5_3 = beepers.get((5, 3), 0)
    total_beepers = sum(count for count in beepers.values() if count > 0)

    if beeper_count_at_5_3 != 0:
        score = 0
        feedback.append("Karel did not pick up the beeper at (5,3).")

    if total_beepers != 0:
        score = 0
        feedback.append(f"Unexpected beepers remain in the world (total={total_beepers}).")

    # Check Karel final position (avenue=2, street=4) and orientation (facing east)
    k = getattr(world, 'karel', None)
    if k is None:
        score = 0
        feedback.append("Could not find Karel instance to check final position and orientation.")
    else:
        if (k.avenue, k.street) != (2, 4):
            score = 0
            feedback.append(f"Karel final position expected (2,4), found ({k.avenue},{k.street}).")
        if not k.facing_east():
            score = 0
            feedback.append("Karel must be facing east at the end.")

    if score == 100:
        return 100, ["Correct: beeper at (5,3) picked up and Karel at (2,4) facing east"]
    return score, feedback
