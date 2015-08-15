import sys
import pygame
import os
from pygame.locals import *

class Bubble(pygame.sprite.Sprite):

    """
    The Bubble class. This class contains the constructor to create bubbles.
    """

    BLUE_SPRITE = "img/KellyBall.png"
    RED_SPRITE = "img/KellyBall.png"
    GREEN_SPRITE = "img/KellyBall.png"
    YELLOW_SPRITE = "img/KellyBall.png"
    ORANGE_SPRITE = "img/KellyBall.png"
    PURPLE_SPRITE = "img/KellyBall.png"

    CENTER = [350, 510]

    INT_TO_TYPE = {0 : BLUE_SPRITE, 1 : RED_SPRITE, 2:GREEN_SPRITE, 3: YELLOW_SPRITE, 4:ORANGE_SPRITE, 5:PURPLE_SPRITE}

    def __init__(self, type):
        """
        This constructor creates an instance of a Bubble. It begins by calling the super class constructor
        Sprite.__init__. This class allows for access to built in functions such as getting it's position and
        detecting for collisions. Afterwards, it loads the image. The pygame.image.load takes in a path and uses
        it to create an image from that source. Refer to the dictionary above for the correspondence. The self.rect
        function uses a method from the super class to get the current x and y coordinates. These can be modified
        as shown in the following step where self.rect[0] and [1] are changed so that the Bubble begins at the flower's
        center.

        :param type: The type of the bubble. Refer to dictionary above for the correspondence.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.INT_TO_TYPE[type])
        self.type = type
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = self.CENTER[0], self.CENTER[1]
        self.speed = [0, 0]
        self.area = pygame.display.get_surface().get_rect()

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > self.area.width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 5 or self.rect.bottom > self.area.height:
            self.speed[1] = 0
            self.speed[0] = 0

class Shooter(pygame.sprite.Sprite):
    SHOOTER_SPRITE = "img/Arrow.jpg"
    CENTER = [360, 495]
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.SHOOTER_SPRITE)
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = self.CENTER[0], self.CENTER[1]

class Board():
    delta = {
        pygame.K_LEFT: (-10, 0),
        pygame.K_RIGHT: (+10, 0),
        pygame.K_UP: (0, -10),
        pygame.K_DOWN: (0, +10),
        }
    WIDTH, HEIGHT = 480, 720
    BACKGROUND = "img/GrassyField.png"
    FOREGROUND = "img/GrassyFieldForeground.png"
    DELTA_Y =  -10

    def __init__(self):
        pygame.init()
        self.bg = pygame.image.load(self.BACKGROUND)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        self.toon = Bubble(0)
        self.shooter =Shooter()
        self.foreground = pygame.image.load(self.FOREGROUND)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.toon.image, self.toon.rect)
        self.screen.blit(self.shooter.image, self.shooter.rect)
        self.screen.blit(self.foreground, (0, 0))
        pygame.display.flip()
    def rot_center(self,image, angle):
        """rotate a Surface, maintaining position."""
        rot_image = pygame.transform.rotate(image, angle)
        loc = rot_image.get_rect().center
        rot_sprite = pygame.transform.rotate(image, angle)
        rot_sprite.get_rect().center = loc
        return rot_sprite
    def event_loop(self):
        toon = self.toon
        delta_x=0
        while True:
            for event in pygame.event.get():


                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        delta_x += -1
                        self.shooter.image = self.rot_center(self.shooter.image, 2)
                    elif event.key == pygame.K_RIGHT:
                        delta_x += 1
                        self.shooter.image = self.rot_center(self.shooter.image, -2)
                    elif event.key == pygame.K_SPACE:
                        toon.speed[0] += delta_x
                        toon.speed[1] += self.DELTA_Y
                        delta_x = 0


            toon.update()

            self.draw()
            pygame.time.delay(10)

if __name__ == '__main__':
    app = Board()
    app.event_loop()