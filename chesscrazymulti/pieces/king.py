class King():
    images=['images/blackking.png','images/whiteking.png']
    def __init__(self,color,type):
        self.color=color
        self.source=self.images[self.color]
        self.opp_color=1 if self.color==0 else 0
        self.type=type
    def get_moves(self,board,id):
        moves=[]
        targets=[]
        possible_moves=[(id[0]-1,id[1]-1),(id[0]-1,id[1]),(id[0]-1,id[1]+1),(id[0],id[1]-1),(id[0],id[1]+1),(id[0]+1,id[1]-1),(id[0]+1,id[1]),(id[0]+1,id[1]+1)]
        keys=list(board[0].keys())+list(board[1].keys())
        for move in possible_moves:
            if ((move[0] in range(8)) and (move[1] in range(8))):
                if move in keys:
                    if move in board[self.opp_color]:
                        targets.append(move)
                else:
                    moves.append(move)         
        return moves,targets
        
                
        