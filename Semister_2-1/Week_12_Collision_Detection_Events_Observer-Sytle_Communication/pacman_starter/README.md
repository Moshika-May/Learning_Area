# Week 12 Exercise: Collision Detection, Events, and Observer-Style Communication

This lab exercise teaches **Euclidean Distance Collision Detection**, **Pygame Custom Events**, and **Decoupled Observer-Style Communication** in the **Pacman Arena**:

- **AABB vs Radial Collision**: Understand why standard axis-aligned bounding box (`pygame.Rect.colliderect`) checks trigger false-positive phantom collisions at empty diagonal corners, and implement accurate Euclidean center-to-center distance checking ($\sqrt{\Delta x^2 + \Delta y^2} < r_1 + r_2$).
- **Strict Architectural Separation**: Collision detection functions must only detect physical contact and post **factual events** (`pygame.event.post()`) to the event queue. They **MUST NOT** import, reference, or call score, sound, or HUD subsystems directly.
- **Custom Pygame Events with Payloads**: Define custom event constants as `pygame.USEREVENT` offsets (`PELLET_EATEN`, `CHERRY_EATEN`, `GHOST_HIT`, `PACMAN_DEFEAT`) and package event attributes in `pygame.event.Event(type, payload_dict)`.
- **Observer Pattern (`EventObserver(ABC)`)**: Enforce a formal single-method contract (`handle_event(event) -> None`) implemented by decoupled subsystems:
  - `ScoreManager`: Tracks total points and collectible counts.
  - `SoundManager`: Synthesizes or plays audio feedback with safe fail-soft fallbacks.
  - `HUDManager`: Renders score, life icons, and feedback messages.
- **Open/Closed Principle (OCP)**: Add a new `AchievementManager` observer (unlocking badges like `"FIRST_BITE"`, `"SWEET_TOOTH"`, `"SURVIVOR"`) with **ZERO** modifications to existing collision code.
- **Collection Mutation Safety**: Safely iterate over active entities using slice copying (`pellets[:]`) and clean up inactive items at frame boundary via list comprehension deferral (`[p for p in pellets if p.active]`).

---

## Files in this Directory

| File | Purpose |
| :--- | :--- |
| **`starter.py`** | **Student Starter Code** — Guided challenges (Tasks 1–6) with TODO stubs, hints, and automated test suite. |
| **`exercise_solution.py`** | **Reference Solution** — Complete working implementation with full entity hierarchy, audio synthesis, HUD, and automated checks. |

---

## Run the Verification Checks

You can run the automated verification suite directly from the repository root. Both scripts support headless environments (including environments without `pygame` installed via an integrated mock):

```bash
# Verify the reference solution:
python3 code/week12/exercise_solution.py --check

# Test your starter implementation:
python3 code/week12/starter.py --check
```

The automated checks verify:
1. `distance_collision()` accurately eliminates AABB diagonal corner phantom hits.
2. `distance_collision()` triggers when sprites are within radius sum contact threshold.
3. Custom event constants are properly defined as `pygame.USEREVENT` offsets.
4. `EventObserver` enforces an abstract `handle_event(self, event)` method.
5. `ScoreManager` accumulates points and stats from custom event payloads.
6. `SoundManager` records and plays sound cues fail-softly in headless environments.
7. `AchievementManager` satisfies the Open/Closed Principle without collision code edits.
8. `check_collisions()` emits facts to the event queue and deactivates entities.
9. List comprehension deferral safely cleans up collections without skipping elements.

---

## Interactive Demonstration

Run the visual Pygame arena (requires `pygame` or `pygame-ce`):

```bash
# In an environment with pygame installed:
python3 code/week12/exercise_solution.py

# Or run using the project virtual environment:
.venv/bin/python3 code/week12/exercise_solution.py
```

Use the **Arrow keys** or **WASD** to control Pacman, eat pellets (+10 pts), grab the bonus bobbing cherry (+50 pts), and dodge the patrolling ghost!

---

## Lab Defense Questions

> **Question 1 (Collision Geometry):** *Why does `pygame.Rect.colliderect` produce false-positive collisions for circular sprites approaching each other diagonally, and how does Euclidean distance solve this problem?*
>
> **Question 2 (Architectural Decoupling):** *Why is it considered bad architectural practice for a collision detection function to directly call `score_manager.add_score(10)` or `sound_manager.play_chomp()`? How does emitting an event to Pygame's event queue satisfy the Single Responsibility and Open/Closed principles?*
