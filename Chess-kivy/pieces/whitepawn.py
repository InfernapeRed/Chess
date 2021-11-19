class WhitePawn():
    def __init__(self):
        self.source='images/whitepawn.png'
        
    def get_moves(self,board):
        board.append(('this is added',1))
        return [(6,6),(7,7)],[(0,0),(7,0)]