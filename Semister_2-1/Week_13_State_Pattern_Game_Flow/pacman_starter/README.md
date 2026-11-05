# Week 13 Lab: State Pattern and Game Flow

SF211: Object-Oriented Programming with Pygame  
Thammasat School of Engineering (TSE)

---

## Overview

In previous weeks, games ran in a single monolithic loop. As games grow to include title screens, gameplay, pause overlays, and game-over screens, managing screen state with boolean flags (`is_menu`, `is_paused`, `is_gameover`) quickly degrades into **"flag soup"** and giant `if/elif/else` switch statements that violate the **Open/Closed Principle (OCP)**.

In this lab, you will apply the Gang of Four (GoF) **State Pattern** combined with a **State Stack** to model game flow cleanly in the Pacman Arena:
- Screen transitions are encapsulated in polymorphic `GameState` subclasses (`TitleMenuState`, `PlayState`, `PauseState`, `GameOverState`).
- The `Game` context delegates `handle_events()`, `update()`, and `draw()` to the active state.
- A **State Stack** allows non-destructive overlays: pressing `[P]` pushes `PauseState` over `PlayState`, keeping gameplay memory intact and frozen until resumed via `pop_state()`.
- The exact same State Pattern is also applied to Ghost AI (`ChaseState`, `ScatterState`, `FrightenedState`, `EatenState`), illustrating design pattern versatility.

---

## Repository Files

- `code/week13/starter.py`: Student scaffold with TODO implementation tasks.
- `code/week13/exercise_solution.py`: Reference implementation with full test coverage and playable demonstration.
- `code/week13/README.md`: This lab guide.

---

## Lab Tasks

1. **Task 1 (`GameState` ABC Contract):**
   Inherit from `ABC` and decorate `handle_event()`, `update()`, and `draw()` with `@abstractmethod` to define the state lifecycle contract.
2. **Task 2 (`Game` Context Stack Methods):**
   Implement `change_state()` (exit old, replace top, enter new), `push_state()` (append, enter), and `pop_state()` (pop, exit, resume previous).
3. **Task 3 (`TitleMenuState` Input):**
   Transition to `PlayState` when `[SPACE]` is pressed; quit via `self.game.quit()` on `[Q]`.
4. **Task 4 (`PlayState` State Transitions):**
   - **4a:** Push `PauseState` on `[P]`, return to `TitleMenuState` on `[ESC]`, and forward steering to `self.pacman.handle_input(event)`.
   - **4b:** Transition to `GameOverState(self.game, self.score)` when `self.lives <= 0`.
5. **Task 5 (`PauseState` Resume):**
   Pop `PauseState` off the stack on `[P]` or `[ESC]` via `self.game.pop_state()`, returning control to `PlayState` with score and lives preserved intact.
6. **Task 6 (`FrightenedState` Ghost AI Timer):**
   Decrease countdown timer, move ghost away from Pacman at half speed, and automatically revert to `ChaseState` when the timer expires.

---

## Verification & Execution

### Run automated verification suite (headless):
```bash
python3 code/week13/starter.py --check
python3 code/week13/exercise_solution.py --check
```

### Launch interactive Pacman Arena:
```bash
python3 code/week13/exercise_solution.py
```

### Controls:
- **Title Screen:** `[SPACE]` to start game, `[Q]` to quit.
- **Gameplay:** Arrow keys / WASD to steer Pacman, `[P]` to pause, `[ESC]` for menu.
- **Pause Screen:** `[P]` or `[ESC]` to resume.
- **Game Over Screen:** `[R]` to restart directly, `[M]` to return to main menu.

---

## Oral Defense Questions

1. **State Pattern vs Boolean Flags:**
   *Why is a polymorphic State Stack superior to boolean flags (`is_paused`, `is_gameover`) when adding new game screens (e.g. `HighScoresState` or `ShopState`)?*

2. **Stack vs Single State:**
   *Why does `PauseState` use `game.push_state()` rather than `game.change_state()`, and what happens to `PlayState`'s variables (score, positions) while paused?*

3. **Open/Closed Principle:**
   *How does the State Pattern allow introducing a new Ghost AI mode without modifying the existing `Ghost` class code?*
