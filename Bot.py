import random
from Common import Direction

class BotIF:
    def __init__(self):
        pass

    def Move(self):
        pass

class RandomBot(BotIF):
    def Move(self):
        move = random.randint(0, 4)
        if move == 0:
            return Direction.UP
        if move == 1:
            return Direction.DOWN
        if move == 2:
            return Direction.LEFT
        if move == 3:
            return Direction.RIGHT