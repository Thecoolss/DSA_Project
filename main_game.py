from hfunctions import *
from greedy import minimax

def main_entry():
    rows = 6
    columns = 7
    numbers_row = "1 2 3 4 5 6 7"
    game_grid = [['*' for _ in range(columns)] for _ in range(rows)]
    heights = [0 for _ in range(columns)]

    game_mode = int(input("VS Player: 1 or VS Bot: 2 : "))
    player_1 = "#"
    player_2 = "O"
    current_player = 1

    # move history stacks for undo/redo
    move_history = []  # stores tuples (row, col, symbol)
    redo_stack = []

    if game_mode == 1:
        game_going = True
        while game_going:
            print_grid(numbers_row, game_grid)

            if current_player == 1:
                result = perform_move(player_1, heights, game_grid, rows, columns, move_history, redo_stack)
                if result is None:
                    # User chose to quit
                    print("Game aborted by player.")
                    return
                if result is False:
                    print_grid(numbers_row, game_grid)
                    print("Player 1 Wins!")
                    break
                game_going = result
                current_player = 2

            else:
                result = perform_move(player_2, heights, game_grid, rows, columns, move_history, redo_stack)
                if result is None:
                    print("Game aborted by player.")
                    return
                if result is False:
                    print_grid(numbers_row, game_grid)
                    print("Player 2 Wins!")
                    break
                game_going = result
                current_player = 1

            if all(height == rows for height in heights):
                print_grid(numbers_row, game_grid)
                print("It's a draw!")
                break

    elif game_mode == 2:
        game_going = True
        current_player = 1

        while game_going:
            print_grid(numbers_row, game_grid)
            if current_player == 1:
                result = perform_move(player_1, heights, game_grid, rows, columns, move_history, redo_stack)
                if result is None:
                    print("Game aborted by player.")
                    return
                if result is False:
                    print_grid(numbers_row, game_grid)
                    print("Player 1 Wins!")
                    break
                game_going = result
                current_player = 2
            else:
                av_moves = available_moves(heights, rows)
                if not av_moves:
                    print_grid(numbers_row, game_grid)
                    print("It's a Draw!")
                    break

                # Greedy bot: try immediate win, block opponent, center preference
                col = bot_move(player_2, player_1, heights, game_grid, rows, columns)

                # Fallback: try minimax if greedy didn't pick (or if more advanced strategy desired)
                if col is None:
                    col = minimax(player_2, player_1, heights, game_grid, rows, columns, True, 4)

                if col is None:
                    print_grid(numbers_row, game_grid)
                    print("It's a Draw!")
                    break

                r, c = make_move_on_grid(col, player_2, game_grid, heights, rows)
                move_history.append((r, c, player_2))
                # New bot move invalidates redo stack
                redo_stack.clear()

                if check_game_over((r, c), game_grid, rows, columns):
                    print_grid(numbers_row, game_grid)
                    print("Bot Wins!")
                    break
                current_player = 1



if __name__ == "__main__":
    main_entry()
