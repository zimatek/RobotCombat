import pygame
import numpy as np


class Projectile(pygame.sprite.Sprite):
    """
        A class to handle the projectiles. They inherit from the class pygame.sprite.Sprite.

        ...

        Attributes
        ----------
        size: tuple
            (with, height) information
        color: tuple
            (r, g, b) color for the projectile
        width: float
            with of the coin (2 * radius)
        height: float
            height of the coin (2 * radius)
        pos: np.array
            x and y position of the coin sprite
        image:
            the image object of the coin.
        rect:
            the rect object of the coin
        velocity: numpy.array
            velocity vector for the projectile
        speed: float
            maximum speed of the projectile
        damage: float
            damage that the projectile carries
    """

    def __init__(self, sx, sy, speed, damage, tx=None, ty=None, angle=None, color=None, size=None):
        pygame.sprite.Sprite.__init__(self)

        if size is None:
            self.__size = (8, 8)
        else:
            self.__size = size

        if color is None:
            self.__color = (98, 0, 255)
        else:
            self.__color = color

        image = pygame.Surface(self.__size)
        image.fill(self.__color)

        self.__image = image
        self.__rect = self.__image.get_rect()
        self.__rect.x, self.__rect.y = sx, sy

        self.__pos = np.array([sx, sy])
        self.__width = self.__rect.width
        self.__height = self.__rect.height
        self.__velocity = np.zeros(2)
        self.__speed = speed
        self.__damage = damage

        if angle is None:
            distance = np.sqrt((tx-sx)**2 + (ty-sy)**2)
            self.__set_velocity(self.__speed * (tx-sx) / distance, self.__speed * (sy-ty) / distance)
        else:
            self.__set_velocity(self.__speed * np.cos(angle), self.__speed * np.sin(angle))

        self.__inner_time = 0

    @property
    def damage(self):
        return self.__damage

    @property
    def pos(self):
        return self.__pos

    @property
    def velocity(self):
        return self.__velocity

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def __set_velocity(self, vx=None, vy=None):
        """
        sets the velocity of the projectile

        :param vx: float or None
        :param vy: float or None
        :return: velocity vector
        """
        if vx is not None:
            self.__velocity[0] = np.clip(vx, - self.__speed, self.__speed)
        if vy is not None:
            self.__velocity[1] = np.clip(vy, - self.__speed, self.__speed)
        return self.__velocity

    def __draw_tail(self, surface):

        if self.__inner_time % 10 > 3:
            tail = pygame.Rect(self.__rect.x + (-1)**int(self.__velocity[0] >= 0) * self.__size[0],
                               self.__rect.y,
                               *self.__size)
            pygame.draw.rect(surface, self.__color, tail)
        if self.__inner_time % 5 > 3:
            tail = pygame.Rect(self.__rect.x + (-1)**int(self.__velocity[0] >= 0) * 2 * self.__size[0],
                               self.__rect.y,
                               *self.__size)
            pygame.draw.rect(surface, self.__color, tail)

    def __die(self):
        self.kill()
        del self

    def move(self, combat):
        """
        Moves the projectile according to its velocity vector.
        """

        dx, dy = self.__set_velocity()

        if self.__pos[0] < 0:
            self.__pos[0] = 0
            self.__die()

        elif self.__pos[0] > combat.dims[0] - self.__rect.width:
            self.__pos[0] = combat.dims[0] - self.__rect.width
            self.__die()

        if self.__pos[1] < 0:
            self.__pos[1] = 0
            self.__die()
        elif self.__pos[1] > combat.dims[1] - self.__rect.height:
            self.__pos[1] = combat.dims[1] - self.__rect.height
            self.__die()

        self.__pos[0] += dx
        self.__pos[1] -= dy

        self.__rect.x = int(self.__pos[0])
        self.__rect.y = int(self.__pos[1])

    def draw(self, surface):
        self.__draw_tail(surface)

    def update(self, combat):
        self.move(combat=combat)
        self.__inner_time += 1
