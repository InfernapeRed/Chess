from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from pieces.whitepawn import WhitePawn
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
        if not self.parent.selected_piece and self.piece:
            self.parent.selected_piece=(self,self.piece)
            self.button.background_color=[0,0,1,1]
            self.parent.update()
            return True
        elif self.parent.selected_piece and (self.button.background_color==[1,1,0,1] or self.button.background_color==[1,0,0,1]):
            if self.piece:
                self.parent.board.remove((self,self.piece))
                self.remove_widget(self.img)
            self.piece=self.parent.selected_piece[1]
            self.parent.board.remove(self.parent.selected_piece)
            self.parent.selected_piece[0].button.background_color=[0,1,0,1] if (self.parent.selected_piece[0].id[0]+self.parent.selected_piece[0].id[1])%2!=0 else [1,1,1,1]
            self.parent.selected_piece[0].remove_widget(self.parent.selected_piece[0].img)
            self.parent.selected_piece[0].piece=None
            self.parent.selected_piece=None
            self.parent.board.append((self,self.piece))
            self.blit_piece()
            self.parent.update()
            return True
    def blit_piece(self):
        if self.piece:
            self.img=Image(source=self.piece.source)
            self.add_widget(self.img)
class New_Board(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board=[]
        self.theme=None
        self.cube_dict={}
        self.selected_piece=None
        self.move=None
        self.moves=None
        self.targets=None
        self.gen_board()
    def gen_board(self):
        a=[(WhitePawn(),(1,1)),(WhitePawn(),(2,2)),(WhitePawn(),(3,3))]
        for i in range(8):
            for j in range(8):
                piece=None
                for k in a:
                    if k[1]==(i,j):
                        piece=k[0]
                color=[0,1,0,1] if (i+j)%2!=0 else [1,1,1,1]
                cube=CubeWidget(color,(i,j),piece)
                self.add_widget(cube)
                self.cube_dict[cube.id]=cube
                if piece:
                    self.board.append((cube,piece))
                    
    def update(self):
        if self.selected_piece:#cube,piece
            self.moves,self.targets=self.selected_piece[1].get_moves(self.board.copy())
            for i in self.moves:
                cube=self.cube_dict[i]
                cube.button.background_color=[1,1,0,1]
            for i in self.targets:
                cube=self.cube_dict[i]
                cube.button.background_color=[1,0,0,1]
        else:
            for a in self.board:
                print(a[0].id)
            print('-----------')
            for i in self.moves:
                cube=self.cube_dict[i]
                cube.button.background_color=[0,1,0,1] if (cube.id[0]+cube.id[1])%2!=0 else [1,1,1,1]
            for i in self.targets:
                cube=self.cube_dict[i]
                cube.button.background_color=[0,1,0,1] if (cube.id[0]+cube.id[1])%2!=0 else [1,1,1,1]
        
        
            
        
class MyChessApp(App):
    def build(self):
        board=New_Board()
        return board
           
MyChessApp().run()