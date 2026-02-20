
import sys
import subprocess
import re
import time

def run_game(student_file, valid_inputs=True):
    """
    Simulates a game of Nimm.
    If valid_inputs is False, we will inject some invalid inputs to test validation.
    """
    proc = subprocess.Popen(
        [sys.executable, "-u", student_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )

    stones = 20
    player = 1
    
    # We will automate a game.
    # Strategy: Player 1 always takes 1. Player 2 always takes 2.
    # 20 -> P1 takes 1 -> 19
    # 19 -> P2 takes 2 -> 17
    # 17 -> P1 takes 1 -> 16
    # 16 -> P2 takes 2 -> 14
    # ...
    # This ensures game progresses.
    
    # We need to read output line by line or chunk? 
    # Readline is safer if we expect newlines. Use a helper.
    
    def read_until_prompt(proc, timeout=2):
        buffer = ""
        start_time = time.time()
        while time.time() - start_time < timeout:
            char = proc.stdout.read(1)
            if not char:
                break
            buffer += char
            # Heuristic: Prompt usually ends with ? or : 
            # "remove 1 or 2 stones? " or "Please enter 1 or 2: "
            if buffer.strip().endswith("?") or buffer.strip().endswith(":"):
                # But allow reading a bit more if it's just a space?
                # input() usually flushes prompt.
                return buffer
        return buffer

    try:
        failure_msg = None
        game_over = False
        
        # Depending on complexity, we simply iterate until we detect "win"
        
        while stones > 0:
            # Expect "There are X stones left."
            # Then "Player Y would you like to remove..."
            
            # Read output until we get a prompt
            output = read_until_prompt(proc)
            
            # Check for win condition in output early?
            if "wins!" in output or "win" in output.lower():
                game_over = True
                break
                
            # Verify stone count
            # Regex: "There are (\d+) stones left"
            m = re.search(r"There are (\d+) stones left", output)
            if not m:
                # failure, or maybe it split across reads?
                # But read_until_prompt should define the chunk.
                return False, f"Expected 'There are {stones} stones left.', but got output:\n{output}"
            
            seen_stones = int(m.group(1))
            if seen_stones != stones:
                 return False, f"Expected {stones} stones left, but program said {seen_stones}. Output:\n{output}"
            
            # Verify Player Turn
            # "Player (\d)"
            m2 = re.search(r"Player (\d)", output)
            if not m2:
                return False, f"Expected 'Player {player}...', could not find player number in output:\n{output}"
            
            seen_player = int(m2.group(1))
            if seen_player != player:
                return False, f"Expected Player {player} turn, but program said Player {seen_player}. Output:\n{output}"
            
            # Decide move
            move = 1
            if not valid_inputs and stones == 19:
                 # Inject bad input once
                 bad_input = "5"
                 proc.stdin.write(f"{bad_input}\n")
                 proc.stdin.flush()
                 
                 # Expect retry prompt
                 # "Please enter 1 or 2: "
                 retry_output = read_until_prompt(proc)
                 if "Please enter 1 or 2" not in retry_output and "1 or 2" not in retry_output:
                     return False, f"Entered invalid move {bad_input}, expected retry prompt containing '1 or 2', got:\n{retry_output}"
                 
                 # Now send valid
                 valid_inputs = True # Reset so we don't loop forever
                 move = 1
            
            # Send move
            proc.stdin.write(f"{move}\n")
            proc.stdin.flush()
            
            stones -= move
            player = 2 if player == 1 else 1
            
            # Loop continues to next turn
        
        # After loop (stones <= 0)
        # We expect a win message if not already seen.
        if not game_over:
            # Read remaining
            rest, _ = proc.communicate(timeout=1)
            output += rest
            if "wins!" not in output and "win" not in output.lower():
                return False, "Game finished but no winner declared."
        
        # Verify winner
        # Last player to take stone loses.
        # If loop ended, stones became <= 0.
        # The player who just moved (previous loop iter) took the last stone.
        # Suppose stones=1. Player 1 takes 1. stones=0. Player 1 was the one who moved.
        # So Player 1 loses. Player 2 wins.
        # We updated `player` var at end of loop.
        # So `player` variable now holds the winner (the one who didn't move last).
        
        expected_winner = player
        # Regex for "Player (\d) wins"
        m_win = re.search(r"Player (\d) wins", output)
        if not m_win:
             return False, f"Could not find 'Player X wins!' message. Output:\n{output}"
        
        actual_winner = int(m_win.group(1))
        if actual_winner != expected_winner:
             return False, f"Expected Player {expected_winner} to win, but Player {actual_winner} won. Output:\n{output}"
            
    except Exception as e:
        proc.kill()
        return False, f"Error running game: {e}"
        
    return True, "Success"
    

def grade(student_file):
    failures = []
    
    # Test 1: Standard Game
    ok, msg = run_game(student_file, valid_inputs=True)
    if not ok: failures.append(msg)
    
    # Test 2: Invalid Inputs
    ok, msg = run_game(student_file, valid_inputs=False)
    if not ok: failures.append(msg)
    
    if failures:
        return 0, failures
        
    return 100, ["Great job! Your Nimm game works perfectly."]
