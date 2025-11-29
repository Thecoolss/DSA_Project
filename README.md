## Connect 4 — Program Flow and Components

### Overview
- Console-based Connect 4 supporting Player vs Player and Player vs Bot.
- Core data structures:
  - `game_grid` (rows × columns 2D list) holds symbols or `*` for empty.
  - `heights` (1D list) tracks how many pieces are in each column for O(1) drop/undo.
  - `move_history` and `redo_stack` store moves for undo/redo.

### File Roles
- `hfunctions.py`: Board utilities (printing, legality checks, move apply/undo/redo, win detection), tactical bot, BFS threat solver.
- `greedy.py`: Heuristic scoring of moves and a greedy bot selector using a heap.
- `new_try.py`: Stronger bot using depth-limited DFS with beam search and cached heuristics/threats.
- `ui_game.py`: Pygame-based graphical UI for playing (Player vs Player or Player vs Bot).
- `main_game.py`: Entry point; orchestrates modes, turns, user I/O, and bot routing.

### Program Flow (start to finish)
1. **Start (`main_game.main_entry`)**
   - Initialize board (`game_grid`, `heights`) for a 6×7 board.
   - Prompt for mode: `1` = Player vs Player; `2` = Player vs Bot.
   - Prepare move history stacks for undo/redo.

2. **Turn Loop (shared structure)**
   - Print board via `hfunctions.print_grid`.
   - If human turn: `hfunctions.perform_move` handles input (`number`, `u/undo`, `r/redo`, `q/quit`), validates moves, updates histories, and returns game-over/quit status.
   - Check for draw if all `heights` reach `rows`.

3. **Player vs Player specifics**
   - Alternate `perform_move` between Player 1 (`#`) and Player 2 (`O`).
   - After each move, `hfunctions.check_game_over` determines a win; loop breaks on win or draw.

4. **Player vs Bot specifics**
   - Human is Player 1 (`#`); bot is Player 2 (`O`).
   - Bot move selection pipeline:
     1. **DFS Beam Bot** (`new_try.dfs_beam_bot_move`):
        - Depth-limited adversarial DFS with beam pruning (default depth 4, beam width 3 in `main_game.py`).
        - Orders moves by heuristic, includes threat-aware ordering, and caches board evaluations.
        - Uses `hfunctions.bfs_threat_solver` to estimate shortest win distances for both sides.
     2. **Greedy fallback** (`greedy.greedy`):
        - Immediate win check, block check, then heap-based best heuristic move using `greedy.score_move`.
     - (Commented-out quick tactical bot remains in code as reference.)
   - Bot move applied with `hfunctions.make_move_on_grid`, logged to history, redo stack cleared.
   - `hfunctions.check_game_over` checks for bot win; otherwise turn returns to human.

5. **Undo/Redo Support**
   - `perform_move` accepts `u/undo` and `r/redo`.
   - `hfunctions.undo_move` and `redo_move` update grid, heights, and histories consistently.
   - In bot games, undo reverts bot move plus previous human move to maintain turn order.

6. **Threat Detection**
   - `hfunctions.bfs_threat_solver` uses BFS to compute the minimum plies to a win for each side (within a depth limit), memoized to avoid recomputation. This influences the DFS bot heuristic.

### Key Algorithms and Complexity Notes
- Move legality (`check_legal_move`) and apply/undo/redo: O(1).
- Available moves (`available_moves`): O(columns).
- Win detection (`check_game_over`): O(1) bounded checks.
- Greedy scoring (`score_move`): O(1) per move (fixed directions).
- DFS beam search bot: O((beam_width)^depth * columns) in worst case within depth limit; uses caching to reduce repeated evaluation.
- BFS threat solver: Up to O(columns^depth) within its depth cap; cached per state.

### Running the Game
```bash
# Text mode
python main_game.py

# Graphical UI
python ui_game.py
```
Follow prompts:
- Choose `1` (PvP) or `2` (PvBot).
- Enter column numbers (1–7). Use `u`/`undo`, `r`/`redo`, or `q`/`quit` as needed.

### Environment setup
- Preferred: use conda with `environment.yml` (now pulls pygame from conda-forge):
  ```bash
  conda env update -f environment.yml
  conda activate connect4_game
  ```
- If you must use pip and have build tools/SDL installed, try `python -m pip install pygame`, but conda-forge is more reliable for pygame binaries.
