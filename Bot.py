import random
from Common import Direction

class BotIF:
    def __init__(self):
        self.goal = None

    def Move(self):
        pass
    
    def AddGoal(self, goal):
        self.goal = goal
    
    def AddBody(self, body):
        self.body = body 
    
    def AddMap(self, map):
        self.map = map 

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

class ClosestRouteBot(BotIF):
    def Move(self):
        xPos, yPos = self.body.Position()[0]
        xGoal, yGoal = self.goal.Position()
        xDist = abs(xPos - xGoal)
        yDist = abs(yPos - yGoal)
        if xDist > yDist:
            if xPos > xGoal:
                if(not self.map.IsCollision((xPos - 1, yPos), self.body)):
                    return Direction.LEFT
                else:
                    return self.TryClosest(xPos, yPos)
            else:
                if(not self.map.IsCollision((xPos + 1, yPos), self.body)):
                    return Direction.RIGHT
                else:
                    return self.TryClosest(xPos, yPos)
        else:
            if yPos > yGoal:
                if(not self.map.IsCollision((xPos, yPos - 1), self.body)):
                    return Direction.UP
                else:
                    return self.TryClosest(xPos, yPos)
            else:
                if(not self.map.IsCollision((xPos, yPos + 1), self.body)):
                    return Direction.DOWN
                else:
                    return self.TryClosest(xPos, yPos)
    
    def TryClosest(self, x, y):
        if(not self.map.IsCollision((x - 1, y), self.body)):
            return Direction.LEFT
        if(not self.map.IsCollision((x, y + 1), self.body)):
            return Direction.DOWN
        if(not self.map.IsCollision((x + 1, y), self.body)):
            return Direction.RIGHT
        if(not self.map.IsCollision((x, y - 1), self.body)):
            return Direction.UP
        return Direction.LEFT