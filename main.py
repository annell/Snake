import pygame
from pygame.locals import *
import random
from enum import Enum
import gym
 
class App:
    def __init__(self):
        self._running = True
        self._close = False
        self._display_surf = None
        self.size = self.weight, self.height = 800, 800
        self.fps = 15
        self.playtime = 0.0
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        pygame.init()
 
    def on_init(self):
        cols = 50
        rows = 50
        mapSizeX = 700
        mapSizeY = 700
        imageSize = (int(mapSizeX/cols), int(mapSizeY/rows))
        self.map = Map(50, 50, mapSizeX, mapSizeY, cols, rows)
        self.snake = Snake(cols/2, rows/2, imageSize)
        self.apple = Apple(cols, rows, imageSize)
        pygame.display.set_caption("Snake")
        self._display_surf = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        self._running = True
        self.font = pygame.font.SysFont('mono', 14, bold=True)
        self.fontEndscore = pygame.font.SysFont('mono', 32, bold=True)
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._close = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.snake.Direction(Direction.RIGHT)
            elif event.key == pygame.K_LEFT:
                self.snake.Direction(Direction.LEFT)
            elif event.key == pygame.K_DOWN:
                self.snake.Direction(Direction.DOWN)
            elif event.key == pygame.K_UP:
                self.snake.Direction(Direction.UP)
            elif event.key == pygame.K_ESCAPE:
                self._close = True
            elif event.key == pygame.K_r:
                self.on_init()

    def on_loop(self):
        pass
    def on_render(self):
        self._display_surf.fill((90, 90, 90))
        #Map
        self.map.Draw(self._display_surf)

        #Scoreboard
        self.draw_text("SCORE: {}".format(len(self.snake.Position())), (0,0))
        self.draw_text("Press R to restart", (0, 13))
        self.draw_text("Press ESC to exit", (0, 26))

        #Snake
        self.snake.Draw(self._display_surf, self.map)
            
        #Apple
        self.apple.Draw(self._display_surf, self.map)
        
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( not self._close ):
            for event in pygame.event.get():
                self.on_event(event)
            if self._running:
                self.snake.Move()
                if self.map.CheckCollision(self.snake, self.apple):
                    self._running = False
                else:
                    self.on_loop()
                    self.on_render()
            else:
                self.fontEndscore.size("Game over! Score: {}".format(len(self.snake.Position())))
                text = self.fontEndscore.render("Game over! Score: {}".format(len(self.snake.Position())), True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.weight/2, self.height/2))
                self._display_surf.blit(text, text_rect)
            self.playtime += self.clock.tick(self.fps) / 1000.0
            pygame.display.flip()

        self.on_cleanup()
    
    def draw_text(self, text, position):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (255, 255, 255))
        self._display_surf.blit(surface, position)

class Direction(Enum):
    UP = "UP"
    DOWN  = "DOWN"
    RIGHT = "RIGHT"
    LEFT = "LEFT"

class Map:
    def __init__(self, x0, y0, width, height, rows, cols):
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.music = "Snake\\music.mp3"
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.imgGrass = pygame.image.load("Snake\\ground.png")
        self.imgStone = pygame.image.load("Snake\\stone.png")
        imageSize = (int(width/cols), int(height/rows))
        self.imgGrass = pygame.transform.scale(self.imgGrass, imageSize)
        self.imgStone = pygame.transform.scale(self.imgStone, imageSize)
        self.mapDetails = []
        for x in range(0, rows*cols):
            self.mapDetails.append(random.random())
    
    def MapToWindow(self, position):
        xMap, yMap = position
        width = self.width / self.cols
        height = self.height / self.rows
        x = self.x0 + width * xMap
        y = self.y0 + height * yMap
        return (x, y, width, height)
    
    def CheckCollision(self, snake, apple):
        snakePositions = snake.Position()
        applePosition = apple.Position()

        if snakePositions[0] == applePosition:
            snake.Food()
            apple.Place()
            while apple.Position() in snake.Position():
                apple.Place()
            return False
        headX, headY = snakePositions[0]
        if headX >= self.cols or headX < 0:
            return True

        if headY >= self.rows or headY < 0:
            return True
        
        if snakePositions.count(snakePositions[0]) > 1:
            return True
        return False
    
    def GridSize(self):
        return (self.width / self.cols, self.height / self.rows)
    
    def Position(self):
        return (self.x0, self.y0, self.width, self.height)
    
    def Draw(self, surface):
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


class Apple:
    def __init__(self, maxX, maxY, imageSize):
        self.maxX = maxX - 1
        self.maxY = maxY - 1
        self.img = pygame.image.load('Snake\\apple.png')
        self.sound = "Snake\\applespawn.wav"
    
        self.img = pygame.transform.scale(self.img, imageSize)
        self.Place()
    
    def Place(self):
        self.x = random.randint(0, self.maxX)
        self.y = random.randint(0, self.maxY)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.sound), maxtime=1000)

    def Position(self):
        return (self.x, self.y)
    
    def Draw(self, surface, map):
        surface.blit(self.img, map.MapToWindow(self.Position())[:2:])

class Snake:
    def __init__(self, x, y, imageSize):
        self.positions = [(x, y)]
        self.x = x
        self.y = y
        self.direction = Direction.RIGHT
        self.oldDirection = self.direction
        self.angleHead = 0
        self.angleTail = 0
        self.gotFood = True
        self.head = pygame.image.load("Snake\\snakehead.png")
        self.head = pygame.transform.scale(self.head, imageSize)
        self.tail = pygame.image.load("Snake\\snaketail.png")
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

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()