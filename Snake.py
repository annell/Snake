import pygame
from Common import Direction

class Snake:
    def __init__(self, x, y, imageSize, headless):
        self.headless = headless
        self.positions = [(x, y)]
        self.x = x
        self.y = y
        self.direction = Direction.RIGHT
        self.oldDirection = self.direction
        self.angleHead = 0
        self.angleTail = 0
        self.gotFood = True
        if not self.headless:
            self.head = pygame.image.load("snakehead.png")
            self.head = pygame.transform.scale(self.head, imageSize)
            self.tail = pygame.image.load("snaketail.png")
            self.tail = pygame.transform.scale(self.tail, imageSize)
    
    def Direction(self, direction):
        self.direction = direction
    
    def Move(self):
        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        elif self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1

        newPosition = (self.x, self.y)
        self.positions.insert(0, newPosition)
        if not self.gotFood:
            self.positions.pop()
        self.gotFood = False
        
        return newPosition
    
    def Food(self):
        self.gotFood = True
    
    def Position(self):
        return self.positions
    
    def Draw(self, surface, map):
        if self.headless:
            return
        if self.oldDirection != self.direction:
            if self.oldDirection == Direction.LEFT:
                self.head = pygame.transform.flip(self.head, True, False)

            self.oldDirection = self.direction
            self.head = pygame.transform.rotate(self.head, -self.angleHead)
            if self.direction == Direction.UP:
                self.angleHead = 90
            if self.direction == Direction.DOWN:
                self.angleHead = 270
            if self.direction == Direction.RIGHT:
                self.angleHead = 0
            if self.direction == Direction.LEFT:
                self.head = pygame.transform.flip(self.head, True, False)
                self.angleHead = 0
            self.head = pygame.transform.rotate(self.head, self.angleHead)            
        
        endX, endY = self.Position()[-1]
        bodyX, bodyY = self.Position()[-2]
        self.tail = pygame.transform.rotate(self.tail, -self.angleTail)
        if endX < bodyX:
            self.angleTail = 0
        elif endX > bodyX:
            self.angleTail = 180
        elif endY < bodyY:
            self.angleTail = 270
        elif endY > bodyY:
            self.angleTail = 90
        self.tail = pygame.transform.rotate(self.tail, self.angleTail)

        first = True 
        for position in self.Position():
            if first:
                surface.blit(self.head, map.MapToWindow(position)[:2:])
                first = False
            elif position == self.Position()[-1]:
                surface.blit(self.tail, map.MapToWindow(position)[:2:])
            else:
                pygame.draw.rect(surface, (0, 255, 0), map.MapToWindow(position))