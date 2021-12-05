import socket
import pickle

class Network():
    def __init__(self,username,addr):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server=addr[0]
        self.port=addr[1]
        self.addr=(self.server,self.port)
        self.username=username
    def send(self,data):
        data=pickle.dumps(data)
        self.client.sendall(data)        
    def connect(self):
        self.client.connect(self.addr)
        self.client.sendall(pickle.dumps(self.username))
        return pickle.loads(self.client.recv(8192))
    def recv(self):
        self.client.sendall(pickle.dumps(0))
        return pickle.loads(self.client.recv(8192))