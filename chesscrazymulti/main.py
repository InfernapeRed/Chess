from kivy.app import App
from kivy.core.text import markup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from pieces import rook,queen,king,bishop,knight,whitepawn,blackpawn
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition,Screen
from kivy.graphics import Color,Ellipse,Rectangle
from kivy.clock import Clock
from network import Network
from kivy.metrics import dp
class CubeWidget(ButtonBehavior,RelativeLayout):
    def __init__(self,color,id,piece,**kwargs):
        self.initcolor=color
        self.id=id
        self.piece=piece
        self.move_state=False
        super(CubeWidget,self).__init__(**kwargs) 
        #self.button=self.ids.button
        #self.button.bind(on_press=self.on_click)
        self.blit_piece()
    def on_click(self):
        if self.parent.turn==self.parent.pairing_screen.color and not self.parent.selected_piece and self.piece and self.parent.turn==self.piece.color:
            if self.parent.selected_crazy:
                self.parent.selected_crazy[0].canvas.before.get_group('color')[0].rgba=self.parent.selected_crazy[0].initcolor
                self.parent.selected_crazy=None
                self.parent.disable_colors()
            self.parent.selected_piece=(self,self.piece)
            self.canvas.before.get_group('color')[0].rgba=self.parent.theme[1][2] if self.initcolor==self.parent.theme[1][0] else self.parent.theme[1][3]
            self.parent.update()
            return True
        elif self.parent.selected_piece and self.move_state:
            self.parent.pairing_screen.data[self.parent.pairing_screen.color]['move']=[self.parent.selected_piece[0].id,self.id]
            self.parent.pairing_screen.network.send(self.parent.pairing_screen.data)
            return True
        elif (self.parent.selected_piece and self.piece) and self.piece.color==self.parent.selected_piece[1].color:
            self.parent.selected_piece[0].canvas.before.get_group('color')[0].rgba=self.parent.selected_piece[0].initcolor
            self.parent.selected_piece=(self,self.piece)
            self.canvas.before.get_group('color')[0].rgba=self.parent.theme[1][2] if self.initcolor==self.parent.theme[1][0] else self.parent.theme[1][3]
            self.parent.disable_colors()
            self.parent.update()
            return True
        elif self.parent.selected_crazy and self.move_state:
            self.parent.pairing_screen.data[self.parent.pairing_screen.color]['crazy_move']=[self.parent.crazybar[self.parent.pairing_screen.color].buttons.index(self.parent.selected_crazy[0]),self.id]                                            #[buttonindex,cube.id]
            self.parent.pairing_screen.network.send(self.parent.pairing_screen.data)
            #self.parent.crazybar[self.parent.selected_crazy[1].color].move_piece(self,self.parent.selected_crazy)
            return True
    def blit_piece(self):
        if self.piece:
            self.img=Image(source=self.piece.source,size_hint=(.7,.7),pos_hint={'x':.15,'y':.1},allow_stretch=True,keep_ratio=True)
            self.add_widget(self.img)
class NewBoard(GridLayout):
    def __init__(self,headbar,statusbar,pairing_screen, **kwargs):
        self.board=[{},{}]
        self.pairing_screen=pairing_screen
        self.crazy_pieces=[{0:('BP',blackpawn.BlackPawn('BP'),0),1:('BN',knight.Knight(0,'BN'),0),2:('BB',bishop.Bishop(0,'BB'),0),3:('BR',rook.Rook(0,'BR'),0),4:('BQ',queen.Queen(0,'BQ'),0)},
                           {0:('WP',whitepawn.WhitePawn('WP'),0),1:('WN',knight.Knight(1,'WN'),0),2:('WB',bishop.Bishop(1,'WB'),0),3:('WR',rook.Rook(1,'WR'),0),4:('WQ',queen.Queen(1,'WQ'),0)}]
        self.crazybar=[headbar,statusbar]
        self.color=1
        self.theme=[([0,1,0,1],[1,1,1,1]),([239.0/255,218.0/255,181.0/255,255.0/255],[181.0/255,135.0/255,99.0/255,255.0/255],[233.0/255,177.0/255,126.0/255,255.0/255],[191.0/255,121.0/255,69.0/255,255.0/255])]
        self.cube_dict={}
        self.selected_piece=None
        self.selected_crazy=None
        self.turn=1
        self.moves=None
        self.targets=None
        super().__init__(**kwargs)
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
                    self.board[piece.color][cube.id]=(cube,piece)
        #self.headbar.blit_pieces()           
    def update(self):
        if self.selected_piece:#cube,piece
            self.moves,self.targets=self.selected_piece[1].get_moves(self.copy(self.board),self.selected_piece[0].id)
            self.moves,self.targets=self.check_status(self.moves.copy(),self.targets.copy(),self.copy(self.board),self.selected_piece)
            self.enable_colors()
        elif self.selected_crazy:#(button,raw_piece)
            self.moves,self.targets=self.crazybar[self.selected_crazy[1].color].get_moves(self.selected_crazy[1])
            self.moves=self.crazybar[self.selected_crazy[1].color].check_status(self.moves.copy(),self.copy(self.board),self.selected_crazy[1])
            self.enable_colors()
        elif not self.selected_piece:
            if self.turn==self.pairing_screen.color:
                self.disable_colors()
            self.turn=1 if self.turn==0 else 0
            is_checkmate=self.is_checkmate()
    def is_checkmate(self):
        possible_moves=[]
        possible_targets=[]
        for id,piece in self.board[self.turn].items():        
            moves,targets=piece[1].get_moves(self.copy(self.board),id)
            moves,targets=self.check_status(moves,targets,self.copy(self.board),piece)
            possible_moves+=moves
            possible_targets+=targets
        if not possible_moves and not possible_targets:
            for index,piece in self.crazy_pieces[self.turn].items():
                moves,targets=self.crazybar[self.turn].get_moves(piece[1])
                moves=self.crazybar[self.turn].check_status(moves,self.copy(self.board),piece[1])
                possible_moves+=moves
            if not possible_moves:
                piece='White' if self.turn==1 else 'Black'
                print(f'{piece} CHECKMATE!!')
                return True
        return False    
    def check_status(self,moves,targets,board,piece):
        new_moves=[]
        new_targets=[]
        for move in moves:
            #is_illegal=self.is_illegal(move,board.copy(),piece)
            if not self.is_illegal(move,self.copy(board),piece):
                new_moves.append(move)
        for move in targets:
            #is_illegal=self.is_illegal(move,board.copy(),piece)
            if not self.is_illegal(move,self.copy(board),piece):
                new_targets.append(move)
        return new_moves,new_targets
    
    def is_illegal(self,move,board,piece):#piece=(cube,piece)
        board[piece[1].color].pop(piece[0].id)
        if move in board[piece[1].opp_color]:
            board[piece[1].opp_color].pop(move)
        board[piece[1].color][move]=piece
        king,opp_king=self.get_kings(board)
        for id,p in board[piece[1].opp_color].items():
            moves,targets=p[1].get_moves(self.copy(board),id)
            if king in targets:
                return True
        return False
                
    def get_kings(self,board):
        for id,piece in board[1].items():
            if piece[1].type=='WK':
                whiteking=id
        for id,piece in board[0].items():
            if piece[1].type=='BK':
                blackking=id
        king=whiteking if self.turn==1 else blackking 
        opp_king=whiteking if self.turn==0 else blackking  
        return king,opp_king
    
    def move_piece(self,move):
        self.selected_piece=None
        for id,wid in self.cube_dict.items():
            if id==move[0]:
                present_cube=wid
            elif id==move[1]:
                cube=wid
        self.selected_piece=(present_cube,present_cube.piece)
        if cube.piece:
            piece=self.crazybar[cube.piece.opp_color].add_crazy(cube.piece)
            self.crazybar[piece[1].color].blit_piece(piece)#('BP',piece,quantity)
            self.board[cube.piece.color].pop(cube.id)
            cube.remove_widget(cube.img)
        cube.piece=self.selected_piece[1]
        self.board[self.selected_piece[1].color].pop(self.selected_piece[0].id)
        self.selected_piece[0].canvas.before.get_group('color')[0].rgba=self.selected_piece[0].initcolor
        self.selected_piece[0].remove_widget(self.selected_piece[0].img)
        self.selected_piece[0].piece=None
        self.selected_piece=None
        self.board[cube.piece.color][cube.id]=(cube,cube.piece)
        cube.blit_piece()
        self.update()
    def disable_colors(self):
        for i in self.moves:
            self.cube_dict[i].move_state=False
            self.cube_dict[i].canvas.after.remove_group('dot')
        for i in self.targets:
            self.cube_dict[i].move_state=False
            self.cube_dict[i].canvas.after.remove_group('dot')    
    def enable_colors(self):
        for i in self.moves:
            self.cube_dict[i].move_state=True
            with self.cube_dict[i].canvas.after:
                Color(rgba=(0,1,0,1),group='dot')
                Ellipse(group='dot',size=(dp(15),dp(15)),pos=(self.cube_dict[i].center[0]-dp(15.0/2),self.cube_dict[i].center[1]-dp(15.0/2)))
        for i in self.targets:
            self.cube_dict[i].move_state=True
            with self.cube_dict[i].canvas.after:
                Color(rgba=(1,0,0,1),group='dot')
                Ellipse(group='dot',size=(dp(15),dp(15)),pos=(self.cube_dict[i].center[0]-dp(15.0/2),self.cube_dict[i].center[1]-dp(15.0/2))) 
    
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
    def copy(self,board):#board=[{(move):(cube,piece),...},{...}]
        copy_board=[{},{}]
        for i in range(2):
            copy_dict=board[i].copy()
            copy_board[i]=copy_dict
        return copy_board
    
    def ping_server(self,fps):
        if self.pairing_screen.is_credited:
            self.pairing_screen.data=self.pairing_screen.network.recv()
            if not self.pairing_screen.game_started:
                self.pairing_screen.load_table()
                if self.pairing_screen.data[0]['username']!='(EMPTY)' and self.pairing_screen.data[1]['username']!='(EMPTY)':
                    self.pairing_screen.game_started=True
                    self.orientation='lr-tb' if self.pairing_screen.color==1 else 'rl-bt'
                    self.crazybar=[self.crazybar[1],self.crazybar[0]] if self.pairing_screen.color==0 else self.crazybar
                    for i in range(len(self.crazybar)):
                        self.crazybar[i].color=i
                        self.crazybar[i].username=self.pairing_screen.data[i]['username']
                        self.crazybar[i].ids.username.text=self.crazybar[i].username
                    self.pairing_screen.parent.current='board_screen'
            else:
                if self.pairing_screen.data[self.pairing_screen.color]['move_state'] and self.pairing_screen.data[self.turn]['move']:
                    self.move_piece(self.pairing_screen.data[self.turn]['move'])
                elif self.pairing_screen.data[self.pairing_screen.color]['crazy_state'] and self.pairing_screen.data[self.turn]['crazy_move']:
                    self.crazybar[self.turn].move_piece(self.pairing_screen.data[self.turn]['crazy_move'][0],self.pairing_screen.data[self.turn]['crazy_move'][1])#index,move
            
class CrazyPiece(ButtonBehavior,RelativeLayout):
    def __init__(self,**kw):
        self.quantity=0
        self.img=None
        self.initcolor=(.6,.6,.6,1)
        self.label=None
        super(CrazyPiece,self).__init__(**kw)  
    def add_image(self,piece):#('BP',piece,2)
        self.quantity=piece[2]
        self.img=Image(source=piece[1].source,size_hint=(.8,.8),pos_hint={'x':.15,'y':.1},allow_stretch=True,keep_ratio=True)
        self.label=Label(text='[b]' + str(self.quantity) + '[/b]',markup=True,font_size=dp(20),size_hint=(None,None),size=(self.height*.3,self.height*.3))
        with self.label.canvas.before:
            Color(rgba=(1,0,0,1),group='label')
            Rectangle(group='label',size=self.label.size)
        self.add_widget(self.img) 
        self.add_widget(self.label)
    def update_label(self):
        if self.quantity>0:
            self.label.text='[b]' + str(self.quantity) + '[/b]'
        else:
            self.remove_widget(self.label)
            self.remove_widget(self.img)
            self.img=None
            self.label=None
    
class HeadBar(BoxLayout):
    def __init__(self,username,color, **kwargs):
        self.username=username
        self.color=color
        #self.pieces={'BP':blackpawn.BlackPawn('BP'),'BQ':queen.Queen(0,'BQ')}
        super().__init__(**kwargs)
        self.buttons=[self.ids.pawn,self.ids.knight,self.ids.bishop,self.ids.rook,self.ids.queen]
    def place_piece(self,button):
        if self.parent.parent.board.selected_piece:
            self.parent.parent.board.selected_piece[0].canvas.before.get_group('color')[0].rgba=self.parent.parent.board.selected_piece[0].initcolor
            self.parent.parent.board.selected_piece=None
            self.parent.parent.board.disable_colors()
        if button.quantity>0 and self.parent.parent.board.turn==self.color and self.color==self.parent.parent.board.pairing_screen.color:
            if self.parent.parent.board.selected_crazy:
                self.parent.parent.board.selected_crazy[0].canvas.before.get_group('color')[0].rgba=self.parent.parent.board.selected_crazy[0].initcolor
                self.parent.parent.board.disable_colors()
            button.canvas.before.get_group('color')[0].rgba=(1,1,0,1)
            self.parent.parent.board.selected_crazy=(button,self.parent.parent.board.crazy_pieces[self.color][self.buttons.index(button)][1])
            self.parent.parent.board.update()
    def blit_piece(self,piece):
        for index,pie in self.parent.parent.board.crazy_pieces[self.color].items():
            if piece==pie:
                if not self.buttons[index].img:
                    self.buttons[index].add_image(piece)
                else:
                    self.buttons[index].quantity+=1
                    self.buttons[index].update_label()
    def get_moves(self,piece):#
        moves=list(self.parent.parent.board.cube_dict.keys())
        for id,cube in self.parent.parent.board.cube_dict.items():
            if cube.piece:     
                moves.remove(id)
        if piece.type=='BP' or piece.type=='WP':
            new_moves=moves.copy()
            for move in moves:
                if move[0]==0 or move[0]==7:
                    new_moves.remove(move)
            return new_moves,[]
        return moves,[]
    def check_status(self,moves,board,piece):#piece
        new_moves=[]
        for move in moves:
            if not self.is_illegal(self.parent.parent.board.copy(board),move,piece):
                new_moves.append(move)
        return new_moves
    def is_illegal(self,board,move,piece):
        board[piece.color][move]=(self.parent.parent.board.cube_dict[move],piece)
        king,opp_king=self.parent.parent.board.get_kings(board)
        for id,p in board[piece.opp_color].items():
            moves,targets=p[1].get_moves(board,id)
            if king in targets:
                return True
        return False
    def move_piece(self,index,move):#(buttonindex,cube.id)
        cube=self.parent.parent.board.cube_dict[move]
        piece=(self.buttons[index],self.parent.parent.board.crazy_pieces[self.color][index][1])#(button,piece)   
        cube.piece=piece[1]
        self.parent.parent.board.board[piece[1].color][cube.id]=(cube,piece[1])
        piece[0].quantity-=1
        for index,pie in self.parent.parent.board.crazy_pieces[self.color].items():
            if pie[0]==piece[1].type:
                self.parent.parent.board.crazy_pieces[self.color][index]=(pie[0],pie[1],pie[2]-1)
        piece[0].canvas.before.get_group('color')[0].rgba=piece[0].initcolor
        piece[0].update_label()
        self.parent.parent.board.selected_crazy=None
        cube.blit_piece()
        self.parent.parent.board.update()
    def add_crazy(self,piece):#piece object
        convert=[{'WP':'BP','WN':'BN','WB':'BB','WR':'BR','WQ':'BQ'},{'BP':'WP','BN':'WN','BB':'WB','BR':'WR','BQ':'WQ'}]
        for index,pie in self.parent.parent.board.crazy_pieces[self.color].items():
            if pie[0]==convert[self.color][piece.type]:
                self.parent.parent.board.crazy_pieces[self.color][index]=(pie[0],pie[1],pie[2]+1)
                return self.parent.parent.board.crazy_pieces[self.color][index]#('BP',piece,quantity)
class BoardScreen(Screen):
    def __init__(self,pairing_screen, **kw):
        super().__init__(**kw)
        self.layout=BoxLayout(orientation='vertical')
        self.headbar=HeadBar('(EMPTY)',None,size_hint=(1,1))
        self.statusbar=HeadBar('(EMPTY)',None,size_hint=(1,1))
        self.board=NewBoard(self.headbar,self.statusbar,pairing_screen)
        self.layout.add_widget(self.headbar)
        self.layout.add_widget(self.board)
        self.layout.add_widget(self.statusbar)
        self.add_widget(self.layout)
        
class PairingScreen(Screen):
    def __init__(self, **kw):
        self.username=None
        self.game_started=False
        self.color=None
        self.is_credited=False
        super().__init__(**kw)
        self.buttons=[self.ids.button1,self.ids.button2]
    def init_network(self,username,addr):
        self.username=username
        self.network=Network(self.username,addr)#username,(ip,port)ip=str,port=int
        self.data=self.network.connect()
        self.load_table()
    def on_click(self,button,touch):
        if touch.is_double_tap and button.text=='(EMPTY)':
            for i in range(len(self.buttons)):
                if self.buttons[i]==button:
                    self.data[i]['username']=self.username
                    self.data[i]['color']=i
                elif self.data[i]['username']==self.username:
                    self.data[i]['username']='(EMPTY)'
                    self.data[i]['color']=i    
            self.network.send(self.data)    
    def load_table(self):
        for i in range(len(self.data)):
            self.buttons[i].text=self.data[i]['username']            
            if self.data[i]['username']==self.username:
                self.color=self.data[i]['color']
            
class CredentialSCreen(Screen):
    def __init__(self,pairing_screen,**kw):
        self.pairing_screen=pairing_screen
        self.start=False
        super().__init__(**kw)
    def on_click(self,ip,port,username):
        if all([len(ip.text),len(port.text),len(username.text)]):
            try:
                port=int(port.text)
                self.start=True
            except:
                print('enter valid data')
            if self.start:
                self.pairing_screen.init_network(username.text,(ip.text,port))
                self.pairing_screen.is_credited=True
                self.parent.current='pairing_screen'
        
class MyChessApp(App):
    def build(self):
        Window.size=(500,650)
        screen_manager=ScreenManager(transition=SlideTransition())
        pairing_screen=PairingScreen(name='pairing_screen')
        credential_screen=CredentialSCreen(pairing_screen,name='credential_screen')
        board_screen=BoardScreen(pairing_screen,name='board_screen')
        screen_manager.add_widget(credential_screen)
        screen_manager.add_widget(pairing_screen)
        screen_manager.add_widget(board_screen)
        Clock.schedule_interval(board_screen.board.ping_server,1.0/30.0)
        return screen_manager
    
           
MyChessApp().run()