class Rook():
    images=['images/blackrook.png','images/whiterook.png']
    def __init__(self,color,type):
        self.color=color
        self.source=self.images[self.color]
        self.opp_color=1 if self.color==0 else 0
        self.type=type
    def get_moves(self,board,id):
        moves=[]
        targets=[]
        keys=list(board[0].keys())+list(board[1].keys())
        stop=False
        stop2=False
        stop3=False
        stop4=False
        for i in range(1,8):##checking in rows(vertical)
            if id[0]+i<8 and not stop:
                if (id[0]+i,id[1]) in keys:
                    if (id[0]+i,id[1]) in board[self.opp_color]:
                        targets.append((id[0]+i,id[1]))   
                    stop=True
                else:
                    moves.append((id[0]+i,id[1]))
            if id[0]-i>=0 and not stop2:
                if (id[0]-i,id[1]) in keys:
                    if (id[0]-i,id[1]) in board[self.opp_color]:
                        targets.append((id[0]-i,id[1]))
                    stop2=True
                else:
                    moves.append((id[0]-i,id[1]))
        ## checking in cols(horizontal)
        for i in range(1,8):
            if id[1]+i<8 and not stop3:
                if (id[0],id[1]+i) in keys:
                    if (id[0],id[1]+i) in board[self.opp_color]:
                        targets.append((id[0],id[1]+i))
                    stop3=True
                else:
                    moves.append((id[0],id[1]+i))
            if id[1]-i>=0 and not stop4:
                if (id[0],id[1]-i) in keys:
                    if (id[0],id[1]-i) in board[self.opp_color]:
                        targets.append((id[0],id[1]-i))
                    stop4=True
                else:
                    moves.append((id[0],id[1]-i))
        return moves,targets