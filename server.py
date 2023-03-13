import socket
from _thread import *
from game_classes import *
import pickle
# this is the code to create a server which will be in charge of updating clients and connecting them


games = {}
IDs = 0
server = socket.gethostbyname(socket.gethostname())
# need to use a port that's open and mostly safe: 5555, 3141, 6022
port = 5558
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    str(e)


s.listen(2)
# at this point the server would have started/created
print("Waiting for a connection, Server Started")




def Gameclient(conn, gameID, player):
    global IDs
    game = games[gameID]
    players = game.getPlayers()
    for p in players:
        p.updateMoneyAmount(game.moneyAmount())
    conn.send(pickle.dumps(players[player-1]))
    
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            if gameID in games:
                if not data:
                    break
                else:
                    players[player-1] = data

                if player == 1:
                    reply = players[1]
                else:
                    reply = players[0]
                print(f"Player 1: {player[0].getPos()} at {player[0].getLocation()} \n Player 2: {player[1].getPos()} at {player[1].getLocation()}")
                
                conn.sendall(pickle.dumps(reply))

            else:
                break

        # any errors would just break the loop - avoids infinite loops
        except:
            break

    # once the while loop is broken notifies the connection is lost and that the connection closes
    print("Lost connection")
    del games[gameID]
    print(f"Game {gameID} deleted")
    IDs -= 1
    conn.close()



while True:
    conn, address = s.accept()
    print("Connected to: ", address)
    IDs += 1
    gameID = (IDs - 1) // 2
    if IDs % 2 == 1:
        games[gameID] = Game(gameID)
        player = 1
        print("Creating new game", gameID)
        print(games)

    else:
        games[gameID].ready()
        player = 2
        print(games)
        print(IDs)

   # connects new player to the server
    start_new_thread(Gameclient, (conn, gameID, player))


