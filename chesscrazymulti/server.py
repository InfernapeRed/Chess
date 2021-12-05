import socket
import threading
import pickle
#from pyngrok import ngrok

class Server():
    def __init__(self):
        self.SERVER='192.168.0.105'
        self.PORT=5005
        #self.ssh_tunnel=ngrok.connect(self.PORT,"tcp")
        #self.url=self.ssh_tunnel.public_url.split('//')[1].split(':')
        #self.url=(socket.gethostbyname(self.url[0]),int(self.url[1]))
        self.game_started=False
        self.move_state=False
        self.crazy_state=False
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.SERVER,self.PORT))
        #self.CONNECTIONS=[]
        self.server.listen()
        print(f'Server started to listen ip:   and port: ')
        self.data=[{'username':'(EMPTY)','color':0,'move':None,'move_state':False,'crazy_state':False,'crazy_move':None},
                   {'username':'(EMPTY)','color':1,'move':None,'move_state':False,'crazy_state':False,'crazy_move':None}]
    def handle_client(self,conn,addr,username):
        conn.send(pickle.dumps(self.data))
        print(username,self.data)
        while True:
            if not self.game_started:
                if self.data[0]['username']!='(EMPTY)' and self.data[1]['username']!='(EMPTY)':
                    self.game_started=True
            try:
                data=pickle.loads(conn.recv(8192))
                if data:
                    self.data=data
                    print(username,data,self.data)
                    for i in self.data:
                        if i['move']:
                            self.move_state=True
                            break
                        elif i['crazy_move']:
                            self.crazy_state=True
                    if self.move_state:
                        for i in self.data:
                            i['move_state']=True
                    if self.crazy_state:
                        for i in self.data:
                            i['crazy_state']=True
                    continue
            except socket.error as e:
                print(e)
            self.send(conn,username)
    def send(self,conn,username):
        conn.sendall(pickle.dumps(self.data))
        for i in self.data:
            if self.move_state and i['username']==username :
                i['move_state']=False
            elif self.crazy_state and i['username']==username :
                i['crazy_state']=False
        if self.move_state:
            move_states=[]
            for i in self.data:
                move_states.append(i['move_state'])
            if not any(move_states):
                for i in self.data:
                    i['move']=None
                print('move_complete')
                self.move_state=False 
        elif self.crazy_state:
            crazy_states=[]
            for i in self.data:
                crazy_states.append(i['crazy_state'])
            if not any(crazy_states):
                for i in self.data:
                    i['crazy_move']=None
                print('crazy_move_complete')
                self.crazy_state=False        
    def run(self):
        #currentplayer=0
        while True:
            conn,addr=self.server.accept()
            print('Connected client',addr)
            #self.CONNECTIONS.append(conn)
            username=pickle.loads(conn.recv(8192))
            thread=threading.Thread(target=self.handle_client,args=(conn,addr,username))
            thread.start()
            #currentplayer+=1
            
Server().run()