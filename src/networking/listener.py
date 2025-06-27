from sys import stdin
from typing import Tuple

from PodSixNet.Connection import ConnectionListener, connection
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from direct.stdpy.thread import start_new_thread


class ClientChannel(Channel):
    def Network(self, data):
        print("Network data:", data)


class GameServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, localaddr=("0.0.0.0", 12345), *args, **kwargs)
        print("Server launched")

    def Connected(self, channel, addr):
        print("New connection:", addr)


class GameClient(ConnectionListener):
    def __init__(self, host: Tuple[str, int]):
        self.Connect(host)
        print("Chat client started")
        print("Ctrl-C to exit")
        # get a nickname from the user before starting
        print("Enter your nickname: ")
        connection.Send({"action": "nickname", "nickname": stdin.readline().rstrip("\n")})
        # launch our threaded input loop
        t = start_new_thread(self.InputLoop, ())

    def Loop(self) -> None:
        connection.Pump()
        self.Pump()

    def InputLoop(self) -> None:
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        while True:
            connection.Send({"action": "message", "message": stdin.readline().rstrip("\n")})

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_players(self, data) -> None:
        print("*** players: " + ", ".join([p for p in data['players']]))

    def Network_message(self, data) -> None:
        print(data['who'] + ": " + data['message'])

    def Network_connected(self, data) -> None:
        print("You are now connected to the server")

    def Network_error(self, data) -> None:
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data) -> None:
        print('Server disconnected')
        exit()
