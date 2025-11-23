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

    score=125*2**player_count-100*2**opponent_count

   
    return score

def score_move(player,opponent,grid,move,rows,columns):
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
        sum_score+=score_direction(move, dis, player, opponent, grid, rows, columns)
    if move[0]<rows//2:
        sum_score+=2
    if move[1]<columns//2:
        sum_score+=2
    return sum_score
        






def minimax(player, opponent, heights, grid, rows, columns, is_maximizing, depth):
    if depth==0:
        return None
    available_cols=available_moves(heights, rows)
    if not available_cols or depth == 0:
        return None

    if is_maximizing:
        best_score=float('-inf')
        best_col=None
        
        for col in available_cols:
            if heights[col]>=rows:
                continue
            move_made=make_move_on_grid(col,player,grid,heights,rows)
            
            score=minimax(player, opponent, heights, grid, rows, columns, False, depth-1)
            heights[col]-=1
            grid[move_made[0]][move_made[1]]='*'

            if score is None:
                score=score_move(player, opponent, grid, move_made, rows, columns)

            if score > best_score:
                best_score=score
                best_col=col
        if depth==4:
            return best_col
        else:
            return best_score
    else:
        best_score=float('inf')
        best_col=None
        
        for col in available_cols:
            move_made=make_move_on_grid(col,player,grid,heights,rows)
            
            score=minimax(player, opponent, heights, grid, rows, columns, True, depth-1)
            heights[col]-=1
            grid[move_made[0]][move_made[1]]='*'

            if score is None:
                score=score_move(opponent, player, grid, move_made, rows, columns)

            if score < best_score:
                best_score=score
                best_col=col
        return best_score
            
            
