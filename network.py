import socket
import pickle
# this creates a client where the it sends and receives information from the server

# class that creates the network/ represents the client
class Network:
    def __init__(self):
        print("CREATING NETWORK")
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server = socket.gethostbyname(socket.gethostname())   # the servers address
        self.__port = 5558
        self.__address = (self.__server, self.__port)
        self.__game = self.connect()
        print("NETWORK CREATED")

    # returns the clients starting position
    def getGame(self):
        return self.__game

    #  function to connect to the server
    def connect(self):
        try:
            print("TRYING")
            self.__client.connect(self.__address)
            print("DONE")
            return pickle.loads(self.__client.recv(2048))
        except:
            pass

    # send and receives the information to the server, makes it easier for transmission to create a function
    def send(self, player):
        try:
            self.__client.send(pickle.dumps(player))
            return pickle.loads(self.__client.recv(4096))
        except socket.error as e:
            print(e)
