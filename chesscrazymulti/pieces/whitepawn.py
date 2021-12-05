class WhitePawn():
    def __init__(self,type):
        self.source='images/whitepawn.png'
        self.color=1
        self.opp_color=0
        self.type=type
    def get_moves(self,board,id):#[(cube,piece)]  id (row,col)
        targets=[] 
        moves=[]
        keys=list(board[0].keys())+list(board[1].keys())
        if (id[0]-1,id[1]-1) in board[0]:
            targets.append((id[0]-1,id[1]-1))
        if (id[0]-1,id[1]+1) in board[0]:
            targets.append((id[0]-1,id[1]+1))
        if (id[0]-1,id[1]) not in keys:
            moves.append((id[0]-1,id[1]))
        if id[0]==6 and (4,id[1]) not in keys and (id[0]-1,id[1]) in moves:
            moves.append((4,id[1]))
        return moves,targets#(row,column)