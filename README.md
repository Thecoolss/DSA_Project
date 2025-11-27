## Connect 4 — Python implementation

This repository contains a small Connect Four implementation using simple, efficient data structures and helpers.

Key design choices

- 2D list board: `game_grid` (rows × columns) — stores symbols or `*` for empty.
- 1D list `heights`: tracks how many tokens are in each column; lets us compute next free row in O(1) time.
- `move_history` and `redo_stack`: LIFO stacks to support undo/redo commands during a human game.

Algorithms used

- available_moves: linear scan across columns to find non-full columns (O(C)).
- check_game_over: directional checks from last move (bounded to 3 steps each direction → O(1) per direction, constant work).
- Bot (greedy): immediate win -> block opponent -> center preference; optional minimax fallback for deeper strategy.

Complexity summary

- Placing or removing a token in a column: O(1).
- Checking available moves across all columns: O(C) (C = number of columns).
- Win detection per move: constant time bounded scans (O(1)).

Problems found and fixes

- Illegal inputs (out of range / non-numeric) now handled by `perform_move` with helpful prompts.
- Moves on full columns are rejected and ask the player to choose again.
- `undo_move` correctly restores both `game_grid` and `heights`; `redo_move` re-applies a previously undone move.
- Bot will detect a full board and declare a draw rather than crashing — greedy bot returns None if no moves left and `main_game` checks for that.

Usage

Run `main_game.py` and follow prompts; use `u`/`undo` to undo a human move, `r`/`redo` to re-apply an undone move, and `q`/`quit` to abort the game.

