import pygame
import random

class Map:
    def __init__(self, x0, y0, width, height, rows, cols, headless):
        self.headless = headless
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.music = "Media\\music.mp3"
        if not self.headless:
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.imgGrass = pygame.image.load("Media\\ground.png")
            self.imgStone = pygame.image.load("Media\\stone.png")
            imageSize = (int(width/cols), int(height/rows))
            self.imgGrass = pygame.transform.scale(self.imgGrass, imageSize)
            self.imgStone = pygame.transform.scale(self.imgStone, imageSize)
            self.mapDetails = []
            for _ in range(0, rows*cols):
                self.mapDetails.append(random.random())
    
    def MapToWindow(self, position):
        xMap, yMap = position
        width = self.width / self.cols
        height = self.height / self.rows
        x = self.x0 + width * xMap
        y = self.y0 + height * yMap
        return (x, y, width, height)
    
    def IsCollision(self, position, snake):
        x, y = position
        if x >= self.cols or x < 0:
            return True

        if y >= self.rows or y < 0:
            return True
        
        if snake.Position().count(position) > 1:
            return True
        return False
    
    def CheckCollision(self, snake, apple):
        snakePositions = snake.Position()
        applePosition = apple.Position()

        if snakePositions[0] == applePosition:
            snake.Food()
            apple.Place()
            while apple.Position() in snake.Position():
                apple.Place()
            return False
        
        return self.IsCollision(snakePositions[0], snake)
    
    def GridSize(self):
        return (self.width / self.cols, self.height / self.rows)
    
    def Position(self):
        return (self.x0, self.y0, self.width, self.height)
    
    def Draw(self, surface):
        if self.headless:
            return
        n = 0
        for x in range(0, self.cols):
            for y in range(0, self.rows):
                if self.mapDetails[n] > 0.999:
                    surface.blit(self.imgStone, self.MapToWindow((x, y)))
                elif self.mapDetails[n] > 0.9:
                    surface.blit(self.imgGrass, self.MapToWindow((x, y)))
                else:
                    pygame.draw.rect(surface, (255, 255, 255), self.MapToWindow((x, y)))
                n += 1