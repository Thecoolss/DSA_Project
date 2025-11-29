import sys

try:
    import pygame
except ImportError as exc:
    raise SystemExit(
        "pygame is required for the UI. Install via conda: "
        "`conda env update -f environment.yml` or `conda install -c conda-forge pygame`"
    ) from exc

from hfunctions import available_moves, check_game_over, check_legal_move, make_move_on_grid
from greedy import greedy
from new_try import dfs_beam_bot_move


PLAYER_1 = "#"
PLAYER_2 = "O"


class Connect4Pygame:
    def __init__(self, vs_bot: bool):
        self.rows = 6
        self.cols = 7
        self.grid = [["*" for _ in range(self.cols)] for _ in range(self.rows)]
        self.heights = [0 for _ in range(self.cols)]
        self.current = PLAYER_1
        self.vs_bot = vs_bot
        self.game_over = False
        self.winner = None

        pygame.init()
        self.cell = 90
        self.margin = 30
        self.width = self.cols * self.cell
        self.height = self.rows * self.cell + 2 * self.margin
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Connect 4")
        self.font = pygame.font.SysFont("arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("arial", 22)

    def draw_board(self, message: str = ""):
        self.screen.fill((20, 26, 48))
        # Board background
        board_rect = pygame.Rect(0, self.margin, self.width, self.rows * self.cell)
        pygame.draw.rect(self.screen, (30, 90, 180), board_rect)

        for r in range(self.rows):
            for c in range(self.cols):
                center = (c * self.cell + self.cell // 2, self.margin + r * self.cell + self.cell // 2)
                color = (220, 220, 220)
                if self.grid[r][c] == PLAYER_1:
                    color = (255, 76, 76)
                elif self.grid[r][c] == PLAYER_2:
                    color = (255, 214, 10)
                pygame.draw.circle(self.screen, color, center, self.cell // 2 - 8)
        if message:
            text_surf = self.font.render(message, True, (255, 255, 255))
            self.screen.blit(text_surf, (20, 5))
        pygame.display.flip()

    def handle_move(self, col: int, symbol: str):
        if not check_legal_move(col, self.heights, self.rows, self.cols):
            return None
        r, c = make_move_on_grid(col, symbol, self.grid, self.heights, self.rows)
        if check_game_over((r, c), self.grid, self.rows, self.cols):
            self.game_over = True
            self.winner = symbol
        elif all(h == self.rows for h in self.heights):
            self.game_over = True
            self.winner = "Draw"
        return r, c

    def bot_move(self):
        col = dfs_beam_bot_move(PLAYER_2, PLAYER_1, self.heights, self.grid, self.rows, self.cols, depth=4, beam_width=3)
        if col is None:
            col = greedy(PLAYER_2, PLAYER_1, self.heights, self.grid, self.rows, self.cols)
        if col is not None:
            self.handle_move(col, PLAYER_2)

    def run(self):
        clock = pygame.time.Clock()
        msg = "Player 1's turn"
        self.draw_board(msg)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                    x, _ = event.pos
                    col = x // self.cell
                    if self.current == PLAYER_1:
                        move = self.handle_move(col, PLAYER_1)
                        if move is None:
                            msg = "Column full. Try another."
                        else:
                            if self.game_over:
                                msg = "Player 1 wins!" if self.winner == PLAYER_1 else "It's a draw!"
                            else:
                                self.current = PLAYER_2
                                msg = "Player 2's turn" if not self.vs_bot else "Bot's turn"
                    else:
                        move = self.handle_move(col, PLAYER_2)
                        if move is None:
                            msg = "Column full. Try another."
                        else:
                            if self.game_over:
                                msg = "Player 2 wins!" if self.winner == PLAYER_2 else "It's a draw!"
                            else:
                                self.current = PLAYER_1
                                msg = "Player 1's turn"

            # Bot turn outside events to allow immediate response
            if self.vs_bot and not self.game_over and self.current == PLAYER_2:
                self.bot_move()
                if self.game_over:
                    msg = "Bot wins!" if self.winner == PLAYER_2 else "It's a draw!"
                else:
                    self.current = PLAYER_1
                    msg = "Player 1's turn"

            self.draw_board(msg)
            clock.tick(60)


def main():
    try:
        mode = int(input("VS Player: 1 or VS Bot: 2 : "))
    except ValueError:
        mode = 2
    vs_bot = (mode != 1)
    game = Connect4Pygame(vs_bot)
    game.run()


if __name__ == "__main__":
    main()
