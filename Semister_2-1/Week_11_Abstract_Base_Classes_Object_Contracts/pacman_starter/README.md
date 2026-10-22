# Week 11 Exercise: Abstract Base Classes and Object Contracts

This lab exercise teaches **Abstract Base Classes (ABCs)**, the **`@abstractmethod` decorator**, and **Fail-Fast Gatekeeping** in Python by establishing formal object contracts in the **Pacman Arena**:

- **`GameObject(ABC)`**: Formal abstract base class inheriting from `abc.ABC`. Declares abstract methods `update(bounds=None)` and `draw(screen)` that every game entity must implement.
- **`IncompleteCherry`**: An incomplete subclass that implements `update()` but omits `draw()`. Demonstrates how Python's ABC metaclass prevents instantiation with a descriptive `TypeError`.
- **`Cherry`**: Concrete bonus collectible fruit subclass fully satisfying the `GameObject` contract with bobbing animation and rendering.
- **`Pacman`, `Ghost`, `Pellet`**: Concrete entities participating in the contract.
- **Polymorphic Game Loop**: Unified update and draw dispatch across all game objects without any defensive `isinstance()` or `hasattr()` checks.

---

## Files in this Directory

| File | Purpose |
| :--- | :--- |
| **`starter.py`** | **Student Starter Code** — Guided challenges for creating `GameObject(ABC)`, testing `IncompleteCherry`, and implementing concrete `Cherry`. |
| **`exercise_solution.py`** | **Reference Solution** — Complete working implementation with full entity hierarchy, interactive Pacman arena, and automated checks. |

---

## Run the Verification Checks

From the repository root:

```bash
python3 code/week11/exercise_solution.py --check
```

Or test your starter implementation:

```bash
python3 code/week11/starter.py --check
```

The automated checks verify:
1. `GameObject` inherits from `abc.ABC` and defines abstract `update()` and `draw()`.
2. Direct instantiation of `GameObject` raises `TypeError`.
3. Incomplete subclass `IncompleteCherry` raises `TypeError` upon instantiation due to missing `draw()`.
4. Concrete entities (`Pacman`, `Ghost`, `Pellet`, `Cherry`) instantiate cleanly and satisfy the contract.
5. The polymorphic game loop successfully dispatches updates and draws across mixed entities.

---

## Interactive Demonstration

Run the visual Pygame arena:

```bash
python3 code/week11/exercise_solution.py
```

Use arrow keys or WASD to navigate Pacman across the arena and collect the bonus Cherry!

---

## Lab Defense Question

> **Defense Question:** *What error occurs when a subclass does not implement an abstract method, at what exact moment does the error occur, and why is that significantly safer than duck typing?*
