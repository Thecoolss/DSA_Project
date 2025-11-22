def print_grid(numbers_row, game_grid):
    print(numbers_row)
    for row in game_grid:
        print(' '.join(row))


def check_legal_move(pick: int, heights, rows, columns):
    if pick < 0 or pick >= columns:
        return False
    return heights[pick] < rows


def available_moves(heights, rows):
    return [idx for idx, height in enumerate(heights) if height < rows]


def make_move_on_grid(pick, symbol, game_grid, heights, rows):
    row_to_fill = rows - heights[pick] - 1
    game_grid[row_to_fill][pick] = symbol
    heights[pick] += 1
    return row_to_fill, pick


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
        if check_direction(move, dis, game_grid, rows, columns):
            return False
    return True


def perform_move(player, heights, game_grid, rows, columns):
    legal_move = False
    player_pick = None

    while not legal_move:
        try:
            player_pick = int(input("Pick a number to enter:  ")) - 1
        except ValueError:
            continue
        legal_move = check_legal_move(player_pick, heights, rows, columns)

    move_made = make_move_on_grid(player_pick, player, game_grid, heights, rows)
    return check_game_over(move_made, game_grid, rows, columns)


def try_move_wins(col, symbol, heights, game_grid, rows, columns):
    if heights[col] >= rows:
        return False
    r, c = make_move_on_grid(col, symbol, game_grid, heights, rows)
    win = not check_game_over((r, c), game_grid, rows, columns)
    heights[c] -= 1
    game_grid[r][c] = '*'
    return win


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
