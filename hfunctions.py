from collections import deque


# Objective: Display the board state with column headers.
# Explanation: Prints the header row and each grid row, spaced for readability.
# Complexity: Best O(rows*columns); Average O(rows*columns); Worst O(rows*columns). Extra space O(1).
def print_grid(numbers_row, game_grid):
    print(numbers_row)
    for row in game_grid:
        print(' '.join(row))


# Objective: Validate that a chosen column is playable.
# Explanation: Ensures the column index is in range and the column is not full.
# Complexity: Best O(1); Average O(1); Worst O(1). Extra space O(1).
def check_legal_move(pick: int, heights, rows, columns):
    if pick < 0 or pick >= columns:
        return False
    return heights[pick] < rows


# Objective: Return all columns that can accept a new piece.
# Explanation: Scans the heights array and collects indices that are below the row limit.
# Complexity: Best O(columns); Average O(columns); Worst O(columns). Extra space O(columns) for the result list.
def available_moves(heights, rows):
    return [idx for idx, height in enumerate(heights) if height < rows]


# Objective: Drop a piece into a column and update bookkeeping.
# Explanation: Finds the next open row from the bottom, writes the symbol, and increments column height.
# Complexity: Best O(1); Average O(1); Worst O(1). Extra space O(1).
def make_move_on_grid(pick, symbol, game_grid, heights, rows):
    row_to_fill = rows - heights[pick] - 1
    game_grid[row_to_fill][pick] = symbol
    heights[pick] += 1
    return row_to_fill, pick


# Objective: Verify a straight-line run of matching pieces from a move.
# Explanation: Steps up to three cells in a direction to confirm all match the origin; stops on mismatch or bounds.
# Complexity: Best O(1); Average O(1); Worst O(1) (fixed steps). Extra space O(1).
def check_direction(move, dire, game_grid, rows, columns):
    x, y = move
    dx, dy = dire
    for i in range(1, 4):
        pos_x = x + dx * i
        pos_y = y + dy * i
        if pos_x < rows and pos_y < columns and pos_x >= 0 and pos_y >= 0:
            if game_grid[pos_x][pos_y] != game_grid[x][y]:
                return False
        else:
            return False
    return True


def check_game_over(move, game_grid, rows, columns):
    """Objective: Determine if the latest move produced a connect-4.

    Explanation: Counts contiguous matching symbols in four primary directions both forward and backward; win when any count reaches 4+.
    Complexity: Best O(1); Average O(1); Worst O(1) (constant directions/steps). Extra space O(1).
    """
    x, y = move
    directions = [
        (1, 0),  # down / up
        (0, 1),  # right / left
        (1, 1),  # down-right / up-left
        (1, -1), # down-left / up-right
    ]

    symbol = game_grid[x][y]
    for dx, dy in directions:
        count = 1
        # forward direction
        for i in range(1, 4):
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < rows and 0 <= ny < columns and game_grid[nx][ny] == symbol:
                count += 1
            else:
                break

        # backward direction
        for i in range(1, 4):
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < rows and 0 <= ny < columns and game_grid[nx][ny] == symbol:
                count += 1
            else:
                break

        if count >= 4:
            return True

    return False


# Objective: Handle a player's turn including input, undo/redo, and move placement.
# Explanation: Processes commands, validates moves, updates histories, and returns game-over/quit status.
# Complexity: Best O(1); Average O(rows*columns) with typical prompt/print cycles; Worst O(rows*columns) with multiple retries. Extra space O(rows*columns) cumulatively for histories.
def perform_move(player, heights, game_grid, rows, columns, move_history=None, redo_stack=None):
    if move_history is None:
        move_history = []
    if redo_stack is None:
        redo_stack = []

    while True:
        prompt = "Pick a number to enter (1-{0}) or 'u' undo, 'r' redo: ".format(columns)
        entry = input(prompt).strip().lower()

        # quit
        if entry in ("q", "quit", "exit"):
            print("Quitting game")
            # return None to indicate the user intentionally quit (distinct from a game-over)
            return None

        # undo
        if entry in ("u", "undo"):
            if not move_history:
                print("Nothing to undo")
                continue

            last = move_history[-1]
            # If last move belongs to the player, undo a single move as before.
            if last[2] == player:
                undo_move(heights, game_grid, move_history, redo_stack)
                print("Undid last move")
                # After undo the human player should pick again (same turn)
                print_grid(' '.join(str(i + 1) for i in range(columns)), game_grid)
                continue

            # If last move is NOT the player's (likely the bot's move when in VS Bot mode),
            # we will undo both moves (bot then player's previous move) so the human can
            # try a different move. This prevents single-stepping bot moves.
            if len(move_history) < 2:
                print("Cannot undo bot move as there is no prior player move to revert")
                continue

            prev = move_history[-2]
            if prev[2] != player:
                # If the move before the bot is not the player's, refuse to undo to avoid
                # inconsistent states.
                print("Undo would not revert a player move — aborting undo")
                continue

            # Undo bot move then undo player's previous move (both push to redo_stack)
            undo_move(heights, game_grid, move_history, redo_stack)
            undo_move(heights, game_grid, move_history, redo_stack)
            print("Undid bot and previous player move — pick a new move")
            print_grid(' '.join(str(i + 1) for i in range(columns)), game_grid)
            continue

        # redo
        if entry in ("r", "redo"):
            if not redo_stack:
                print("Nothing to redo")
                continue
            redo_move(heights, game_grid, move_history, redo_stack, rows)
            print("Redid move")
            # After redo the turn is considered finished, check for game-over
            last = move_history[-1]
            return not check_game_over((last[0], last[1]), game_grid, rows, columns)

        # numeric move
        try:
            player_pick = int(entry) - 1
        except ValueError:
            print("Invalid input — please enter a number, 'u' (undo) or 'r' (redo)")
            continue

        if not check_legal_move(player_pick, heights, rows, columns):
            print('Illegal move — column full or out of range. Try again.')
            continue

        r, c = make_move_on_grid(player_pick, player, game_grid, heights, rows)
        move_history.append((r, c, player))
        # Any new move invalidates the redo stack
        redo_stack.clear()

        return not check_game_over((r, c), game_grid, rows, columns)


# Objective: Test whether playing in a column yields an immediate win.
# Explanation: Temporarily place a piece, check for victory, then revert the state.
# Complexity: Best O(1); Average O(1); Worst O(1). Extra space O(1).
def try_move_wins(col, symbol, heights, game_grid, rows, columns):
    if heights[col] >= rows:
        return False
    r, c = make_move_on_grid(col, symbol, game_grid, heights, rows)
    # after simulating the move, check_game_over returns True when the move produced a win
    win = check_game_over((r, c), game_grid, rows, columns)
    heights[c] -= 1
    game_grid[r][c] = '*'
    return win


def undo_move(heights, game_grid, move_history, redo_stack=None):
    """Objective: Undo the latest move and optionally store it for redo.

    Explanation: Pops last move, clears the grid cell, adjusts height, and records it in redo_stack when provided.
    Complexity: Best O(1); Average O(1); Worst O(1). Extra space O(1).
    """
    if not move_history:
        return False
    r, c, symbol = move_history.pop()
    game_grid[r][c] = '*'
    heights[c] -= 1
    if redo_stack is not None:
        redo_stack.append((r, c, symbol))
    return True


def redo_move(heights, game_grid, move_history, redo_stack, rows):
    """Objective: Reapply a previously undone move.

    Explanation: Pops from redo_stack and uses make_move_on_grid to place it, keeping histories consistent.
    Complexity: Best O(1); Average O(1); Worst O(1). Extra space O(1).
    """
    if not redo_stack:
        return None
    r, c, symbol = redo_stack.pop()
    # We must place the piece in correct next free row for that column.
    # Use make_move_on_grid so heights are updated consistently.
    # make_move_on_grid expects column index and symbol.
    new_r, new_c = make_move_on_grid(c, symbol, game_grid, heights, rows)
    move_history.append((new_r, new_c, symbol))
    return new_r, new_c


# Objective: Provide a quick tactical bot move (win, block, or center preference).
# Explanation: Checks for immediate wins, then blocks, otherwise favors central columns.
# Complexity: Best O(1) if early return; Average O(columns); Worst O(columns). Extra space O(1).
def bot_move(bot_symb, opp_symb, heights, game_grid, rows, columns):
    cols = available_moves(heights, rows)
    if not cols:
        return None
    for col in cols:
        if try_move_wins(col, bot_symb, heights, game_grid, rows, columns):
            return col
    for col in cols:
        if try_move_wins(col, opp_symb, heights, game_grid, rows, columns):
            return col

    center = [3, 2, 4, 1, 5, 0, 6]
    for col in center:
        if col in cols:
            return col
    return cols[0]


_bfs_cache = {}


def bfs_threat_solver(current_player, opponent, heights, game_grid, rows, columns, max_depth=6):
    """Objective: BFS to find minimum plies to a win for current player and opponent.

    Explanation: Explores alternating-turn game states up to max_depth using a queue; memoizes by state to reuse results. Returns (moves_for_current, moves_for_opponent) or None when not reachable.
    Complexity: Best O(columns) when early win; Average O(columns^depth) within depth; Worst O(columns^depth) within depth. Extra space O(columns^depth) for queue/visited/cache.
    """

    heights_key = tuple(heights)
    grid_key = tuple(tuple(row) for row in game_grid)
    state_key = (
        current_player,
        opponent,
        heights_key,
        grid_key,
        rows,
        columns,
        max_depth,
    )
    if state_key in _bfs_cache:
        return _bfs_cache[state_key]

    start_grid = [row[:] for row in game_grid]
    start_heights = list(heights_key)
    queue = deque()
    queue.append((start_grid, start_heights, current_player, 0))
    seen = set()
    current_best = None
    opponent_best = None

    while queue:
        grid, hs, turn, depth = queue.popleft()
        if depth >= max_depth:
            continue

        node_key = (tuple(hs), turn)
        if node_key in seen:
            continue
        seen.add(node_key)

        cols = available_moves(hs, rows)
        for col in cols:
            g2 = [row[:] for row in grid]
            h2 = hs[:]
            r, c = make_move_on_grid(col, turn, g2, h2, rows)
            win = check_game_over((r, c), g2, rows, columns)
            if win:
                moves_needed = depth + 1
                if turn == current_player:
                    if current_best is None or moves_needed < current_best:
                        current_best = moves_needed
                else:
                    if opponent_best is None or moves_needed < opponent_best:
                        opponent_best = moves_needed
                continue
            queue.append((g2, h2, opponent if turn == current_player else current_player, depth + 1))

    result = (current_best, opponent_best)
    _bfs_cache[state_key] = result
    return result
