import pygame
import random
import sys, getopt
from Map import Map
from Snake import Snake
from Apple import Apple
from Common import Direction
from Bot import RandomBot, ClosestRouteBot
 
class App:
    def __init__(self, headless, bot):
        self.bot = bot
        self.headless = headless
        self._running = True
        self._close = False
        self._display_surf = None
        self.size = self.weight, self.height = 800, 800
        if not self.headless:
            self.fps = 15
            self.playtime = 0.0
            self.clock = pygame.time.Clock()
            pygame.mixer.init()
            pygame.init()
 
    def on_init(self):
        self._running = True
        cols = 50
        rows = 50
        mapSizeX = 700
        mapSizeY = 700
        imageSize = (int(mapSizeX/cols), int(mapSizeY/rows))
        self.map = Map(50, 50, mapSizeX, mapSizeY, cols, rows, self.headless)
        self.snake = Snake(cols/2, rows/2, imageSize, self.headless)
        self.apple = Apple(cols, rows, imageSize, self.headless)
        if self.bot:
            self.bot.AddGoal(self.apple)
            self.bot.AddBody(self.snake)
            self.bot.AddMap(self.map)
        if not self.headless:
            pygame.display.set_caption("Snake")
            self._display_surf = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
            self.font = pygame.font.SysFont('mono', 14, bold=True)
            self.fontEndscore = pygame.font.SysFont('mono', 32, bold=True)
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._close = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if not self.bot:
                    self.snake.SetDirection(Direction.RIGHT)
            elif event.key == pygame.K_LEFT:
                if not self.bot:
                    self.snake.SetDirection(Direction.LEFT)
            elif event.key == pygame.K_DOWN:
                if not self.bot:
                    self.snake.SetDirection(Direction.DOWN)
            elif event.key == pygame.K_UP:
                if not self.bot:
                    self.snake.SetDirection(Direction.UP)
            elif event.key == pygame.K_ESCAPE:
                self._close = True
            elif event.key == pygame.K_r:
                self.on_init()

    def on_render(self):
        if not self.headless:
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
        if not self.headless:
            pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        while( not self._close ):
            if not self.headless:
                for event in pygame.event.get():
                    self.on_event(event)

            if self.bot:
                self.snake.SetDirection(self.bot.Move())

            if self._running:
                self.snake.Move()
                self.snake.Eat(self.apple)
                if self.map.IsCollision((self.snake.x, self.snake.y) ,self.snake):
                    self._running = False
                else:
                    self.on_render()
            elif not self.headless:
                self.fontEndscore.size("Game over! Score: {}".format(len(self.snake.Position())))
                text = self.fontEndscore.render("Game over! Score: {}".format(len(self.snake.Position())), True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.weight/2, self.height/2))
                self._display_surf.blit(text, text_rect)
            else:
                print("Game over! Score: {}".format(len(self.snake.Position())))
                self._close = True
            if not self.headless:
                self.playtime += self.clock.tick(self.fps) / 1000.0
                pygame.display.flip()

        self.on_cleanup()
    
    def draw_text(self, text, position):
        self.font.size(text)
        surface = self.font.render(text, True, (255, 255, 255))
        self._display_surf.blit(surface, position)

def main(argv):
    headless = False
    bot = None
    try:
        opts, args = getopt.getopt(argv,"hgb",["gui-off=","bot-type="])
    except getopt.GetoptError:
        print('main.py -g --gui-off -b --bot')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -g --gui-off -b --bot')
            sys.exit()
        elif opt in ("-g", "--gui-off"):
            headless = True
        elif opt in ("-b", "--bot-type"):
            bot = ClosestRouteBot()
    theApp = App(headless, bot)
    theApp.on_execute()

if __name__ == "__main__":
   main(sys.argv[1:])
