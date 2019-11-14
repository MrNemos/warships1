import random
import warBoard
class Player:
    def __init__(self, name, board):
        self.name = name
        self.board = board

class Game_room:
    def __init__(self, name, players, status):
        self.name = name
        self.players = players
        self.status = status
        self.turn_to_shot = random.choice(players)

    def lobby(self):


    def start(self):
        pass

    def end(self):
        pass

