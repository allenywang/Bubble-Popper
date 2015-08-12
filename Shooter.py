import sys
import pygame
import os
from pygame.locals import *

character = "kellyBall.png"
bg = "bg.png"
justin = "justinEnemy.png"

delta = {
    pygame.K_LEFT: (-10, 0),
    pygame.K_RIGHT: (+10, 0),
    pygame.K_UP: (0, -10),
    pygame.K_DOWN: (0, +10),
    }

class Toon(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(player)
        self.bg = pygame.image.load(bg)
        self.rect = self.image.get_rect()
        self.speed = [2, 2]
        self.area = pygame.display.get_surface().get_rect()
    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > self.area.width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > self.area.height:
            self.speed[1] = -self.speed[1]

class Main(object):
    def __init__(self):
        self.setup()
    def setup(self):
        pygame.init()
        size = (self.width, self.height) = (720,720)
        self.black = (0, 0, 0)
        self.bg = pygame.image.load(bg)
        self.screen = pygame.display.set_mode(size, 0, 32)
        self.toon = Toon(character)
        self.justin = Toon(justin)
        self.setup_background()
    def setup_background(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.toon.image, self.toon.rect)
        self.screen.blit(self.justin.image, self.justin.rect)
        pygame.display.flip()
    def event_loop(self):
        toon = self.toon
        justin = self.toon
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    deltax, deltay = delta.get(event.key, (0, 0))
                    toon.speed[0] += deltax
                    toon.speed[1] += deltay

            toon.speed[0] *= 0.95
            toon.speed[1] *= 0.95
            toon.update()

            justin.update()
            self.draw()
            pygame.time.delay(10)

if __name__ == '__main__':
    app = Main()
    app.event_loop()