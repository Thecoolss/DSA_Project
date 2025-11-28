import heapq
from typing import List, Tuple, Optional

from hfunctions import available_moves, make_move_on_grid, check_game_over, try_move_wins
from greedy import score_move


def dfs_beam_bot_move(
    player: str,
    opponent: str,
    heights: List[int],
    grid: List[List[str]],
    rows: int,
    columns: int,
    depth: int = 5,
    beam_width: int = 4,
) -> Optional[int]:
    """Depth-limited DFS with beam pruning and heuristic leaf scoring.

    - Uses DFS to a fixed depth.
    - At each ply, orders candidate moves by a heuristic (greedy score) and only explores
      the top `beam_width` moves (beam search).
    - Max node = current player, Min node = opponent reply. This is the same adversarial
      idea as minimax but implemented with covered tools: DFS + heaps + pruning.
    """

    def undo_move(r: int, c: int) -> None:
        grid[r][c] = "*"
        heights[c] -= 1

    def evaluate_board() -> int:
        """Heuristic from the bot's perspective: aggregate strength of both sides."""
        total = 0
        for r in range(rows):
            for c in range(columns):
                cell = grid[r][c]
                if cell == player:
                    total += score_move(player, opponent, grid, (r, c), rows, columns)
                elif cell == opponent:
                    total -= score_move(opponent, player, grid, (r, c), rows, columns)
        return total

    def ordered_moves(for_player: str, is_max: bool) -> List[Tuple[int, Tuple[int, int]]]:
        """Return up to beam_width moves ordered by heuristic score using a heap."""
        cols = available_moves(heights, rows)
        if not cols:
            return []

        # If it's the bot's turn, detect opponent threats we must block.
        threat_cols = set()
        if is_max:
            for col in cols:
                if try_move_wins(col, opponent, heights, grid, rows, columns):
                    threat_cols.add(col)

        heap: List[Tuple[int, int, int, int]] = []
        for col in cols:
            if heights[col] >= rows:
                continue
            r, c = make_move_on_grid(col, for_player, grid, heights, rows)
            if check_game_over((r, c), grid, rows, columns):
                undo_move(r, c)
                return [(col, (r, c))]  # immediate win
            h_score = score_move(
                for_player,
                opponent if for_player == player else player,
                grid,
                (r, c),
                rows,
                columns,
            )
            if is_max and col in threat_cols:
                h_score += 100000  # prioritize blocking opponent immediate wins

            # keep beam_width best-scoring moves
            heapq.heappush(heap, (h_score, col, r, c))
            if len(heap) > beam_width:
                heapq.heappop(heap)
            undo_move(r, c)

        # heap currently holds the top-scoring moves (min element is lowest of the kept set)
        best = heapq.nlargest(len(heap), heap)
        return [(col, (r, c)) for (_, col, r, c) in best]

    def search(is_max: bool, current_depth: int) -> int:
        cols = ordered_moves(player if is_max else opponent, is_max)
        if not cols:
            return 0

        best = float("-inf") if is_max else float("inf")
        for col, (r, c) in cols:
            mover = player if is_max else opponent
            make_move_on_grid(col, mover, grid, heights, rows)
            win = check_game_over((r, c), grid, rows, columns)

            if win:
                score = 100000 - (depth - current_depth) if is_max else -100000 + (depth - current_depth)
            elif current_depth == 0:
                score = evaluate_board()
            else:
                score = search(not is_max, current_depth - 1)

            undo_move(r, c)

            if is_max:
                best = max(best, score)
            else:
                best = min(best, score)
        return int(best)

    # Root: decide the best initial column
    # Quick tactical checks at root: take win, then block opponent win.
    root_cols = available_moves(heights, rows)
    for col in root_cols:
        if try_move_wins(col, player, heights, grid, rows, columns):
            return col
    for col in root_cols:
        if try_move_wins(col, opponent, heights, grid, rows, columns):
            return col

    root_moves = ordered_moves(player, True)
    if not root_moves:
        return None

    best_col = root_moves[0][0]
    best_score = float("-inf")
    for col, (r, c) in root_moves:
        make_move_on_grid(col, player, grid, heights, rows)
        win = check_game_over((r, c), grid, rows, columns)
        if win:
            score = 100000
        else:
            score = search(False, depth - 1)
        undo_move(r, c)

        if score > best_score:
            best_score = score
            best_col = col

    return best_col
