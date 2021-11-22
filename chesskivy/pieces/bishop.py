class Bishop():
    images=['images/blackbishop.png','images/whitebishop.png']
    def __init__(self,color,type):
        self.color=color
        self.source=self.images[self.color]
        self.opp_color=1 if self.color==0 else 0
        self.type=type
    def get_moves(self,board,id):
        moves=[]
        targets=[]
        keys=board.keys()
        for i in range(1,8):## checking top right cross
            if id[0]-i>=0 and id[1]+i<8:
                if (id[0]-i,id[1]+i) in keys:
                    if board[(id[0]-i,id[1]+i)][1].color==self.opp_color:
                        targets.append((id[0]-i,id[1]+i))
                    break
                moves.append((id[0]-i,id[1]+i))
        # checking top left corner
        for i in range(1,8):
            if id[0]-i>=0 and id[1]-i>=0:
                if (id[0]-i,id[1]-i) in keys:
                    if board[(id[0]-i,id[1]-i)][1].color==self.opp_color:
                        targets.append((id[0]-i,id[1]-i))
                    break
                moves.append((id[0]-i,id[1]-i))
            
        #checking bottom left corner
        for i in range(1,8):
            if id[0]+i<8 and id[1]-i>=0:
                if (id[0]+i,id[1]-i) in keys:
                    if board[(id[0]+i,id[1]-i)][1].color==self.opp_color:
                        targets.append((id[0]+i,id[1]-i))
                    break
                moves.append((id[0]+i,id[1]-i))
            
        # checking bottom right corner
        for i in range(1,8):
            if id[0]+i<8 and id[1]+i<8:
                if (id[0]+i,id[1]+i) in keys:
                    if board[(id[0]+i,id[1]+i)][1].color==self.opp_color:
                        targets.append((id[0]+i,id[1]+i))
                    break
                moves.append((id[0]+i,id[1]+i))
        #print(moves,targets)
        return moves,targets