from hfunctions import *


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

    if game_mode == 1:
        game_going = True
        while game_going:
            print_grid(numbers_row, game_grid)

            if current_player == 1:
                game_going = perform_move(player_1, heights, game_grid, rows, columns)
                if not game_going:
                    print_grid(numbers_row, game_grid)
                    print("Player 1 Wins!")
                    break
                current_player = 2

            else:
                game_going = perform_move(player_2, heights, game_grid, rows, columns)
                if not game_going:
                    print_grid(numbers_row, game_grid)
                    print("Player 2 Wins!")
                    break
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
                game_going = perform_move(player_1, heights, game_grid, rows, columns)
                if not game_going:
                    print_grid(numbers_row, game_grid)
                    print("Player 1 Wins!")
                    break
                current_player = 2
            else:
                col = bot_move(player_2, player_1, heights, game_grid, rows, columns)
                if col is None:
                    print_grid(numbers_row, game_grid)
                    print("It's a Draw!")
                    break

                r, c = make_move_on_grid(col, player_2, game_grid, heights, rows)
                if not check_game_over((r, c), game_grid, rows, columns):
                    print_grid(numbers_row, game_grid)
                    print("Bot Wins!")
                    break
                current_player = 1

            if all(height == rows for height in heights):
                print_grid(numbers_row, game_grid)
                print("It's a draw!")
                break


if __name__ == "__main__":
    main_entry()
