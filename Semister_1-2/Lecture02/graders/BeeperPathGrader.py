import sys
import runpy

CAPTURED_WORLD = None

import karel.KarelWorld as KW
import karel.stanfordkarel
from karel.Karel import Karel
import os
import glob
import re


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
            world_file = "worlds/BeeperPath.w"

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


def _parse_beepers_from_world(world_file):
    beepers = []
    beeper_re = re.compile(r"Beeper:\s*\((\d+),\s*(\d+)\);\s*(\d+)")
    with open(world_file, "r") as f:
        for line in f:
            m = beeper_re.search(line)
            if m:
                avenue = int(m.group(1))
                street = int(m.group(2))
                count = int(m.group(3))
                beepers.append(((avenue, street), count))
    return beepers


def grade(student_file):
    """Grade BeeperPath solutions.

    Expectations (for every world matching worlds/BeeperPath*.w):
      - World contains a contiguous horizontal beeper path starting at avenue 1 (increasing avenue).
      - Karel ends immediately after the last beeper on the path (i.e., one step past the beeper with maximum avenue) and is facing east.
    """
    global CAPTURED_WORLD

    # Find all BeeperPath world files (support multiple path lengths)
    world_files = sorted(glob.glob("worlds/BeeperPath*.w"))
    if not world_files:
        world_files = ["worlds/BeeperPath.w"]

    failures = []

    for wf in world_files:
        # Reset captured world
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

        # Parse initial beeper layout from the world file to find the last beeper
        initial_beepers = _parse_beepers_from_world(wf)
        if not initial_beepers:
            failures.append(f"{os.path.basename(wf)}: No beepers found in initial world.")
            continue

        # Determine last beeper by maximum avenue (if tie, pick max street among them)
        max_avenue = max(pos[0][0] for pos in initial_beepers)
        candidates = [(pos, cnt) for (pos, cnt) in initial_beepers if pos[0] == max_avenue]
        # pick the candidate with max street (robust for non-horizontal paths)
        last_pos, last_count = max(candidates, key=lambda x: x[0][1])
        last_avenue, last_street = last_pos

        # Validate initial beepers form a horizontal contiguous path starting at avenue 1 on last_street
        expected_positions = [(a, last_street) for a in range(1, max_avenue+1)]
        initial_positions = [pos for (pos,cnt) in initial_beepers]
        missing = [p for p in expected_positions if p not in initial_positions]
        if missing:
            failures.append(f"{os.path.basename(wf)}: Expected contiguous beeper path at {expected_positions}, but missing {missing}.")
            continue

        # Check Karel final position and orientation
        k = getattr(world, 'karel', None)
        if k is None:
            failures.append(f"{os.path.basename(wf)}: Could not find Karel instance to check final position and orientation.")
            continue

        expected_pos = (last_avenue + 1, last_street)
        if (k.avenue, k.street) != expected_pos:
            failures.append(f"{os.path.basename(wf)}: Karel final position expected {expected_pos}, found ({k.avenue},{k.street}).")
            continue

        if not k.facing_east():
            failures.append(f"{os.path.basename(wf)}: Karel must be facing east at the end.")
            continue

    if failures:
        return 0, failures

    return 100, ["Correct: Karel walked along the contiguous beeper path and stopped right after the last beeper facing east for all BeeperPath worlds"]