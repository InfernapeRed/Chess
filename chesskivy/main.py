from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from pieces import rook,queen,king,bishop,knight,whitepawn,blackpawn
from kivy.properties import ObjectProperty
class CubeWidget(RelativeLayout):
    button=ObjectProperty(None)
    def __init__(self,color,id,piece,**kwargs):
        self.id=id
        self.piece=piece
        self.initcolor=color
        super(CubeWidget,self).__init__(**kwargs) 
        self.button.bind(on_press=self.on_click)
        self.blit_piece()
    def on_click(self,button):
        if not self.parent.selected_piece and self.piece and self.piece.color==self.parent.turn:
            self.parent.selected_piece=(self,self.piece)
            self.button.background_color=self.parent.theme[1][2] if self.button.background_color==self.parent.theme[1][0] else self.parent.theme[1][3]
            self.parent.update()
            return True
        elif self.parent.selected_piece and (self.button.background_color==[250.0/255,247.0/255,65.0/255,1] or self.button.background_color==[247.0/255,112.0/255,112.0/255,1]):
            self.parent.move_piece(self)
            return True
        elif (self.parent.selected_piece and self.piece) and self.piece.color==self.parent.selected_piece[1].color:
            self.parent.selected_piece[0].button.background_color=self.parent.theme[1][0] if (self.parent.selected_piece[0].id[0]+self.parent.selected_piece[0].id[1])%2!=0 else self.parent.theme[1][1]
            self.parent.selected_piece=(self,self.piece)
            self.button.background_color=self.parent.theme[1][2] if self.button.background_color==self.parent.theme[1][0] else self.parent.theme[1][3]
            self.parent.disable_colors()
            self.parent.update()
            return True
    def blit_piece(self):
        if self.piece:
            self.img=Image(source=self.piece.source,size_hint=(.7,.7),pos_hint={'x':.15,'y':.1},allow_stretch=True,keep_ratio=True)
            self.add_widget(self.img)
class New_Board(GridLayout):
    def __init__(self, **kwargs):
        self.board={}
        self.theme=[([0,1,0,1],[1,1,1,1]),([239.0/255,218.0/255,181.0/255,255.0/255],[181.0/255,135.0/255,99.0/255,255.0/255],[233.0/255,177.0/255,126.0/255,255.0/255],[191.0/255,121.0/255,69.0/255,255.0/255])]
        self.cube_dict={}
        self.selected_piece=None
        self.turn=1
        self.moves=None
        self.targets=None
        
        super().__init__(**kwargs)
        #print(self.__dict__)
        self.gen_board()
    def gen_board(self):
        a=self.raw_board()
        for i in range(8):
            for j in range(8):
                piece=None
                for k in a:
                    if k[1]==(i,j):
                        piece=(k[0])
                color=self.theme[1][0] if (i+j)%2!=0 else self.theme[1][1]
                cube=CubeWidget(color,(i,j),piece)
                self.add_widget(cube)
                self.cube_dict[cube.id]=cube
                if piece:
                    self.board[cube.id]=(cube,piece)
                    
    def update(self):
        if self.selected_piece:#cube,piece
            self.moves,self.targets=self.selected_piece[1].get_moves(self.board.copy(),self.selected_piece[0].id)
            self.moves,self.targets=self.check_status(self.moves.copy(),self.targets.copy(),self.board.copy(),self.selected_piece)
            self.enable_colors()
        elif not self.selected_piece:
            self.turn=1 if self.turn==0 else 0
            self.disable_colors()
            is_checkmate=self.is_checkmate()
    def is_checkmate(self):
        possible_moves=[]
        possible_targets=[]
        for id,piece in self.board.items():        
            if (piece[1].color==(1 if self.turn==1 else 0)):
                moves,targets=piece[1].get_moves(self.board.copy(),id)
                moves,targets=self.check_status(moves,targets,self.board.copy(),piece)
                possible_moves+=moves
                possible_targets+=targets
        if not possible_moves and not possible_targets:
            piece='White' if self.turn==1 else 'Black'
            print(f'{piece} CHECKMATE!!')
            return True
        return False    
    def check_status(self,moves,targets,board,piece):
        new_moves=[]
        new_targets=[]
        for move in moves:
            is_illegal=self.is_illegal(move,board.copy(),piece)
            if not is_illegal:
                new_moves.append(move)
        for move in targets:
            is_illegal=self.is_illegal(move,board.copy(),piece)
            if not is_illegal:
                new_targets.append(move)
        return new_moves,new_targets
    
    def is_illegal(self,move,board,piece):
        board.pop(piece[0].id)
        board[move]=piece
        king,opp_king=self.get_kings(board)
        for id,piece in board.items():
            if (piece[1].color== (1 if self.turn==0 else 0)):
                moves,targets=piece[1].get_moves(board,id)
                if king in targets:
                    return True
        return False
                
    def get_kings(self,board):
        for id,piece in board.items():
            if piece[1].type=='WK':
                whiteking=id
            if piece[1].type=='BK':
                blackking=id
        king=whiteking if self.turn==1 else blackking 
        opp_king=whiteking if self.turn==0 else blackking  
        return king,opp_king
    
    def move_piece(self,cube):
        if cube.piece:
            self.board.pop(cube.id)
            cube.remove_widget(cube.img)
        cube.piece=self.selected_piece[1]
        self.board.pop(self.selected_piece[0].id)
        self.selected_piece[0].button.background_color=self.theme[1][0] if (self.selected_piece[0].id[0]+self.selected_piece[0].id[1])%2!=0 else self.theme[1][1]
        self.selected_piece[0].remove_widget(self.selected_piece[0].img)
        self.selected_piece[0].piece=None
        self.selected_piece=None
        self.board[cube.id]=(cube,cube.piece)
        cube.blit_piece()
        self.update()
    def disable_colors(self):
        for i in self.moves:
            cube=self.cube_dict[i]
            cube.button.background_color=self.theme[1][0] if (cube.id[0]+cube.id[1])%2!=0 else self.theme[1][1]
        for i in self.targets:
            cube=self.cube_dict[i]
            cube.button.background_color=self.theme[1][0] if (cube.id[0]+cube.id[1])%2!=0 else self.theme[1][1] 
    
    def enable_colors(self):
        for i in self.moves:
            cube=self.cube_dict[i]
            cube.button.background_color=[250.0/255,247.0/255,65.0/255,1]
        for i in self.targets:
            cube=self.cube_dict[i]
            cube.button.background_color=[247.0/255,112.0/255,112.0/255,1] 
    
    def raw_board(self):
        board=[]
        for i in range(8):
            board.append((whitepawn.WhitePawn('WP'),(6,i)))
            board.append((blackpawn.BlackPawn('BP'),(1,i)))
        board2=[(rook.Rook(1,'WR'),(7,0)),(rook.Rook(1,'WR'),(7,7)),(knight.Knight(1,'WN'),(7,1)),(knight.Knight(1,'WN'),(7,6)),
                (bishop.Bishop(1,'WB'),(7,2)),(bishop.Bishop(1,'WB'),(7,5)),(queen.Queen(1,'WQ'),(7,3)),(king.King(1,'WK'),(7,4)),
                (rook.Rook(0,'BR'),(0,0)),(rook.Rook(0,'BR'),(0,7)),(knight.Knight(0,'BN'),(0,1)),(knight.Knight(0,'BN'),(0,6)),
                (bishop.Bishop(0,'BB'),(0,2)),(bishop.Bishop(0,'BB'),(0,5)),(queen.Queen(0,'BQ'),(0,3)),(king.King(0,'BK'),(0,4))]

        return board+board2 
class MyChessApp(App):
    def build(self):
        layout=BoxLayout(orientation='vertical')
        headbar=BoxLayout(size_hint=(1,1))
        statusbar=BoxLayout(size_hint=(1,1))
        board=New_Board()
        layout.add_widget(headbar)
        layout.add_widget(board)
        layout.add_widget(statusbar)
        return layout
           
MyChessApp().run()