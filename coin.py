import pygame
import numpy as np


class Coin(pygame.sprite.Sprite):
    """
        A class to handle the coins. They inherit from the class pygame.sprite.Sprite.

        ...

        Attributes
        ----------
        radius : float
            radius of the coin.
        width: float
            with of the coin (2 * radius)
        height: float
            height of the coin (2 * radius)
        pos: np.array
            x and y position of the coin sprite
        value: float
            the value of the coin object
        image:
            the image object of the coin.
        rect:
            the rect object of the coin
            
    """

    def __init__(self, pos, value=1):
        pygame.sprite.Sprite.__init__(self)

        self.__radius = 8
        self.__width = self.radius * 2
        self.__height = self.radius * 2
        self.__pos = pos
        self.__value = value

        image = pygame.image.load("Resources/coin.png").convert_alpha()
        self.__image = pygame.transform.scale(image, (self.__width, self.__height))
        self.__rect = self.__image.get_rect()
        self.__rect.x, self.__rect.y = self.__pos[0] - self.__radius, self.__pos[1] + self.__radius

    @property
    def value(self):
        return self.__value

    @property
    def radius(self):
        return self.__radius

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def pos(self):
        return self.__pos

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect
