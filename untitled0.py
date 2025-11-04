ROWS=6
COLUMNS=7

   
numbers_row="  1    2    3    4    5    6    7"
game_grid = [
    ['*' for _ in range(COLUMNS)]
    for _ in range(ROWS)
]

def print_grid():
    print(numbers_row)
    for row in game_grid:
        print(row)
    
    
game_mode=int(input("VS Player: 1 or VS Bot: 2 : "))
player_1="#"
player_2="O"
current_player=1
heights=[0,0,0,0,0,0,0]


def check_legal_move(pick:int):
    print(heights[pick])
    return heights[pick]!=ROWS


def make_move_on_grid(pick,symbol):
    #print(COLUMNS-heights[pick],pick)
    game_grid[ROWS-heights[pick]-1][pick]=symbol
    heights[pick]+=1
    return ROWS-heights[pick],pick
    


def check_direction(move,dire):
    #same=True
    x,y=move
    dx,dy=dire
    #print(x,y)
    for i in range(1,4):
        pos_x=x+dx*i
        pos_y=y+dy*i
        #print(pos_x,pos_y)
        if pos_x<ROWS and pos_y<COLUMNS:
            if game_grid[pos_x][pos_y]!=game_grid[x][y]:
                return False
                break
        else:
            return False
        
    return True
        
                
        

def check_game_over(move,symbol):
    displacements=[(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    
    check=False
    for dis in displacements:
        check=check_direction(move,dis)
        if check:
            break
        
    #print(check)
    return not check
    

def perform_move(player):
    legal_move=False
    
    while not legal_move:
        player_pick=int(input("Pick a number to enter:  "))
        legal_move=check_legal_move(player_pick-1)
    
    move_made=make_move_on_grid(player_pick-1,player)
    #print(move_made)
    return check_game_over(move_made,player)
    

if game_mode==1:
    game_going=True
    
    while game_going:
        print_grid()
        
        if current_player==1:
            game_going=perform_move(player_1)
            current_player=2
        
        else:
             game_going=perform_move(player_2)
             
             current_player=1
            
            
            
            
            