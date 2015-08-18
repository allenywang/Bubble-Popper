import sys
import numpy as np
import pygame
import random

class Bubble(pygame.sprite.Sprite):

    """
    The Bubble class. This class contains the constructor to create bubbles.
    """

    BLUE_SPRITE = "img/KellyBall.png"
    RED_SPRITE = "img/StellaBall.png"
    GREEN_SPRITE = "img/KellyBall.png"
    YELLOW_SPRITE = "img/KellyBall.png"
    ORANGE_SPRITE = "img/KellyBall.png"
    PURPLE_SPRITE = "img/KellyBall.png"

    CENTER = [350, 510]

    INT_TO_TYPE = {0 : BLUE_SPRITE, 1 : RED_SPRITE, 2:GREEN_SPRITE, 3: YELLOW_SPRITE, 4:ORANGE_SPRITE, 5:PURPLE_SPRITE}

    def __init__(self, type):
        """
        This constructor creates an instance of a Bubble. This class allows for access to built in functions such
        as getting it's position and detecting for collisions. Afterwards, it loads the image. The pygame.image.load
        takes in a path and uses it to create an image from that source. Refer to the dictionary above for the
        correspondence. The self.rect function uses a method from the super class to get the current x and y
        coordinates. These can be modified as shown in the following step where self.rect[0] and [1] are changed so
        that the Bubble begins at the flower'scenter.

        :param type: The type of the bubble. Refer to dictionary above for the correspondence.
        """

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.INT_TO_TYPE[type])
        self.type = type
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = self.CENTER[0], self.CENTER[1]
        self.speed = [0, 0]
        self.area = pygame.display.get_surface().get_rect()

    def update(self, bubbles):
        """
        Updates the bubble's location. Utilizes pygames function, move, in order to modify the x and y position. This
        also contains the boundaries for the bubble to prevent it from flying off screen.
        """

        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > self.area.width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 5 or self.rect.bottom > self.area.height:
            self.speed = [0, 0]
        if pygame.sprite.spritecollide(self, bubbles, False):
            print(self.speed)
            self.speed = [0, 0]


class Shooter(pygame.sprite.Sprite):
    """
    The shooter class. This class inherits from the pygame Sprite class. You can modify what sprite to use, where the
    center is, and what orientation the shooter is at.
    """

    SHOOTER_SPRITE = "img/Arrow.jpg"
    CENTER = [375, 495]

    def __init__(self):
        """
        The constructor to create a shooter sprite. This initializes the image and centers it. This requires a base
        image because with every rotation, quality is lost. Using the base image and storing the rotation amount
        allows for faster changes in frames and incerased quality.
        """

        self.base = self.image = pygame.image.load(self.SHOOTER_SPRITE)
        self.rect = self.image.get_rect()
        self.rect.center = self.CENTER
        self.rotation = 0

    def rotate(self, rotation):
        """
        Rotates and re-centers the shooter.
        """

        self.rotation+=rotation
        self.image = pygame.transform.rotozoom(self.base, np.degrees(self.rotation), 1)
        self.rect = self.image.get_rect()
        self.rect.center = self.CENTER

    def shoot(self, bubble, angle):
        """
        Shoots the bubble on the board.

        :param bubble: The bubble to be shot.
        """
        bubble.speed[0] += angle
        bubble.speed[1] = -10

class Board():
    """
    The board class. This class specifies the size of the screen, the image background, and the image foreground. It
    also contains all the transitions to update the board.
    """
    WIDTH, HEIGHT = 480, 720
    BACKGROUND = "img/GrassyField.png"
    FOREGROUND = "img/GrassyFieldForeground.png"

    def __init__(self):
        """
        Initializes a board. First loads the image, setups up the screen, creates a shooter object, and adds a
        foreground.
        """

        pygame.init()
        self.bg = pygame.image.load(self.BACKGROUND)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        self.sprites = pygame.sprite.Group()
        self.shooter = Shooter()
        self.foreground = pygame.image.load(self.FOREGROUND)
        pygame.display.flip()

    def update_sprites(self, current_bubble):
        """
        Updates the sprites on the screen. The blit function replaces the areas the sprite takes up with the
        background behind it.
        """

        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(current_bubble.image, current_bubble.rect)
        for sprite in self.sprites:
            self.screen.blit(sprite.image, sprite.rect)
        self.screen.blit(self.shooter.image, self.shooter.rect)
        self.screen.blit(self.foreground, (0, 0))
        pygame.display.flip()

    def main(self):
        current_bubble = Bubble(0)
        bubble_has_been_shot = False
        delta_x=0
        while True:
            current_bubble.update(self.sprites)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        delta_x += -1
                        self.shooter.rotate(0.10)
                    elif event.key == pygame.K_RIGHT:
                        delta_x += 1
                        self.shooter.rotate(-0.10)
                    elif event.key == pygame.K_SPACE:
                        self.shooter.shoot(current_bubble, delta_x)
                        bubble_has_been_shot = True
            current_bubble.update(self.sprites)
            if bubble_has_been_shot and current_bubble.speed == [0, 0]:
                self.sprites.add(current_bubble)
                current_bubble = Bubble(random.randint(0, 5))
                bubble_has_been_shot = False
            self.update_sprites(current_bubble)
            pygame.time.delay(10)

if __name__ == '__main__':
    app = Board()
    app.main()