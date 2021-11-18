from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from pieces.whitepawn import WhitePawn

class CubeWidget(RelativeLayout):
    def __init__(self,color,id,piece,**kwargs):
        self.color=color
        self.id=id
        self.piece=piece
        super().__init__(**kwargs)
        if self.piece:
            self.img=Image(source='whitepawn.png')
            self.add_widget(self.img)
        else:
            self.img=None
    def on_touch_down(self, touch):
        if self.collide_point(touch.x,touch.y):
            print(self.id,self.pos)
            return True
        return super().on_touch_down(touch)    
class New_Board(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board=[]
        self.theme=None
        self.gen_board()
    def gen_board(self):
        a=[(WhitePawn(),1,1),(WhitePawn(),2,2),(WhitePawn(),3,3)]
        for i in range(8):
            for j in range(8):
                color=(0,1,0,1) if (i+j)%2!=0 else (1,1,1,1)
                for k in a:
                    if (k[1],k[2])==(i,j):
                        cube=CubeWidget(color,(i,j),k[0])
                        self.board.append((k[0],cube))
                    else:
                        cube=CubeWidget(color,(0,0),None)
                self.add_widget(cube)
class MyChessApp(App):
    def build(self):
        board=New_Board()
        return board
           
MyChessApp().run()
