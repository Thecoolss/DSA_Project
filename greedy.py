from hfunctions import *
def score_direction(move, dire, player, opponent, grid, rows, columns):
    x, y = move
    dx, dy = dire
    player_count = 0
    opponent_count = 0
    
    for step in range(1, 4):
        nx, ny = x + step * dx, y + step * dy
        if 0 <= nx < rows and 0 <= ny < columns:
            if grid[nx][ny] == player:
                player_count += 1
            elif grid[nx][ny] == opponent:
                opponent_count += 1
        else:
            break

    # Exponential weighting for longer contiguous segments (higher is better)
    score = 125 * (2 ** player_count) - 100 * (2 ** opponent_count)

   
    return score

def score_move(player, opponent, grid, move, rows, columns):
    sum_score=0
    displacements = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ]
    for dis in displacements:
        sum_score += score_direction(move, dis, player, opponent, grid, rows, columns)
    # Favor positions closer to centre of the board
    center_bonus = (columns // 2) - abs(move[1] - (columns // 2))
    sum_score += center_bonus
    return sum_score
        






def greedy(player, opponent, heights, grid, rows, columns, *_args, **_kwargs):
    """Greedy replacement for minimax.

    Signature kept compatible with previous minimax calls. Extra arguments are ignored.

    Returns a column index to play, or None when no valid move exists.
    """
    cols = available_moves(heights, rows)
    if not cols:
        return None

    # 1) immediate win
    for col in cols:
        if try_move_wins(col, player, heights, grid, rows, columns):
            return col

    # 2) block opponent immediate win
    for col in cols:
        if try_move_wins(col, opponent, heights, grid, rows, columns):
            return col

    # 3) score remaining moves and choose best — use insertion sort to order for clarity
    scored = []  # list of tuples (col, score)
    for col in cols:
        if heights[col] >= rows:
            continue
        # simulate move temporarily to score the resulting position
        r, c = make_move_on_grid(col, player, grid, heights, rows)
        s = score_move(player, opponent, grid, (r, c), rows, columns)
        # rollback
        heights[col] -= 1
        grid[r][c] = '*'
        # insertion sort insert into 'scored' keeping descending order
        inserted = False
        for i in range(len(scored)):
            if s > scored[i][1]:
                scored.insert(i, (col, s))
                inserted = True
                break
        if not inserted:
            scored.append((col, s))

    if not scored:
        return None

    # pick the highest scoring column
    best_col = scored[0][0]
    return best_col
            
            
