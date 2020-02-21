import pygame
import random

class Apple:
    def __init__(self, maxX, maxY, imageSize, headless):
        self.headless = headless
        self.maxX = maxX - 1
        self.maxY = maxY - 1
        if not self.headless:
            self.img = pygame.image.load('apple.png')
            self.sound = "applespawn.wav"
            self.img = pygame.transform.scale(self.img, imageSize)
        self.Place()
    
    def Place(self):
        self.x = random.randint(0, self.maxX)
        self.y = random.randint(0, self.maxY)
        if not self.headless:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.sound), maxtime=1000)

    def Position(self):
        return (self.x, self.y)
    
    def Draw(self, surface, map):
        surface.blit(self.img, map.MapToWindow(self.Position())[:2:])
