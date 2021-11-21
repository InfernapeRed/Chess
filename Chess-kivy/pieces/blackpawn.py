class BlackPawn():
    def __init__(self,type):
        self.source='images/blackpawn.png'
        self.color=0
        self.type=type
    def get_moves(self,board,id):#[(cube,piece)]  id (row,col)
        targets=[] 
        moves=[]
        if (id[0]+1,id[1]-1) in board.keys():
            if board[(id[0]+1,id[1]-1)][1].color==1:
                targets.append((id[0]+1,id[1]-1))
        if (id[0]+1,id[1]+1) in board.keys():
            if board[(id[0]+1,id[1]+1)][1].color==1:
                targets.append((id[0]+1,id[1]+1))
        if (id[0]+1,id[1]) not in board.keys():
            moves.append((id[0]+1,id[1]))
        if id[0]==1 and (3,id[1]) not in board.keys() and (id[0]+1,id[1]) in moves:
            moves.append((3,id[1]))
        return moves,targets#(row,column)