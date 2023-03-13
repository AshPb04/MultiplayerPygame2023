import socket
from _thread import *
from game_classes import *
import pickle
# this is the code to create a server which will be in charge of updating clients and connecting them


games = {}
IDs = 0
connected = set()
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




def threaded_client(conn, gameID, player):
    global IDs
    # sends a message to the client once it has successfully connected to the server
    game = games[gameID]
    players = game.getPlayers()
    for p in players:
        p.updateMoneyAmount(game.moneyAmount())
    conn.send(pickle.dumps(players[player-1]))
    # allows the while loop to continuously run while the client is connecting
    while True:
        try:
            # data represents the data that the server would receive from the client
            # 2048 is the amount of bits the server can receive at once, the bigger num longer it takes to receive
            data = pickle.loads(conn.recv(4096))


            # if the data can't be received the while loop will break, prevents infinite while loop
            if gameID in games:
                if not data:
                    print("Disconnected")
                    break
                else:
                    players[player-1] = data

                if player == 1:
                    reply = players[1]
                else:
                    reply = players[0]
                print("Received: ", data)
                print("Sending: ", reply)
                # when a server needs to send back information you need to encode it - safer
                # encodes it into a bytes object, so when client receives the reply they also need to decode it
                conn.sendall(pickle.dumps(reply))

            else:
                break

        # any errors would just break the loop - avoids infinite loops
        except:
            break

    # once the while loop is broken notifies the connection is lost and that the connection closes
    print("Lost connection")
    del games[gameID]
    print(f"{gameID} deleted")
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

    # this creates a thread which allows the function stated to run in the background
    # means that the function does not have to finish executing for the while loop to continue
    start_new_thread(threaded_client, (conn, gameID, player))


