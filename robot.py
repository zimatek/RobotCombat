import pygame
import numpy as np

from projectile import Projectile


class Robot(pygame.sprite.Sprite):
    """
    A class to handle the robot.
    """

    def __init__(self, x, y, turn_left=False,
                 projectile_color=(162, 38, 51), image_path="Resources/simple_robot.png", **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.__projectile_color = projectile_color
        self.__image_path = image_path

        self.__width = 4*32
        self.__height = 4*32
        self.__pos = np.array([x, y])
        self.__velocity = np.zeros(2)

        # Initialize base stats
        self.__base_max_health = kwargs["health"]
        self.__base_armor = kwargs["armor"]
        self.__base_health_regen = kwargs["health_regen"]
        self.__base_damage = kwargs["damage"]
        self.__base_self_speed = kwargs["self_speed"]
        self.__base_projectile_initial_speed = kwargs["projectile_initial_speed"]
        self.__base_projectile_per_second = kwargs["projectile_per_second"]

        # Initialize current stats
        self.__max_health = kwargs["health"]
        self.__armor = kwargs["armor"]
        self.__health_regen = kwargs["health_regen"]
        self.__damage = kwargs["damage"]
        self.__self_speed = kwargs["self_speed"]
        self.__projectile_initial_speed = kwargs["projectile_initial_speed"]
        self.__projectile_per_second = kwargs["projectile_per_second"]

        # Initialize growth statistics
        self.__g_max_health = kwargs["g_health"]
        self.__g_armor = kwargs["g_armor"]
        self.__g_health_regen = kwargs["g_health_regen"]
        self.__g_damage = kwargs["g_damage"]
        self.__g_projectile_per_second = kwargs["g_projectile_per_second"]
        self.__max_self_speed = kwargs["max_self_speed"]
        self.__max_projectile_initial_speed = kwargs["max_projectile_initial_speed"]

        self.__stat_keys = ["damage", "projectile_initial_speed", "projectile_per_second",
                            "self_speed", "armor", "max_health", "health_regen"]

        self.__health = kwargs["health"]
        self.__experience_for_level_up = kwargs["experience_for_level_up"]
        self.__g_experience_for_level_up = kwargs["g_experience_for_level_up"]

        self.__turn_left = turn_left
        self.__time_since_attack = 0

        self.__direction_move = {'up': False, 'down': False, 'right': False, 'left': False}

        self.__experience = 0
        self.__level = 0
        self.__experience_points = 0
        self.__living = True

    @property
    def projectile_initial_speed(self):
        return self.__projectile_initial_speed

    @property
    def self_speed(self):
        return self.__self_speed

    @property
    def max_self_speed(self):
        return self.__max_self_speed

    @property
    def projectile_per_second(self):
        return self.__projectile_per_second

    @property
    def stat_keys(self):
        return self.__stat_keys

    @property
    def health(self):
        return self.__health

    @property
    def damage(self):
        return self.__damage

    @property
    def armor(self):
        return self.__armor

    @property
    def max_health(self):
        return self.__max_health

    @property
    def health_regen(self):
        return self.__health_regen

    @property
    def level(self):
        return self.__level

    @property
    def experience(self):
        return self.__experience

    @property
    def experience_for_level_up(self):
        return self.__experience_for_level_up

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
    def image_path(self):
        return self.__image_path

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def living(self):
        return self.__living

    @property
    def experience_points(self):
        return self.__experience_points

    @property
    def max_projectile_initial_speed(self):
        return self.__max_projectile_initial_speed

    def __heal(self, healing):
        if self.__health <= self.__max_health - healing:
            self.__health += healing
        else:
            self.__health = self.__max_health

    def __get_experience(self, value):
        self.__experience += value
        if self.__experience >= self.__experience_for_level_up:
            self.__level += 1
            self.__experience = self.__experience - self.__experience_for_level_up
            self.__experience_points += 3
            self.__heal(self.__max_health * self.__health_regen / 100)
            self.__experience_for_level_up += self.__g_experience_for_level_up

    def move(self, dx=None, dy=None, combat=None):
        if combat is None:
            raise ValueError("combat is required for Robot.move")

        dx, dy = self.set_velocity(dx, dy)

        if self.__pos[0] < 0:
            self.__pos[0] = 0
        elif self.__pos[0] > combat.dims[0] - self.__rect.width:
            self.__pos[0] = combat.dims[0] - self.__rect.width

        if self.__pos[1] < 0:
            self.__pos[1] = 0
        elif self.__pos[1] > combat.dims[1] - self.__rect.height:
            self.__pos[1] = combat.dims[1] - self.__rect.height

        if dx > 0:
            if self.__turn_left:
                self.flip_x()
        elif dx < 0:
            if not self.__turn_left:
                self.flip_x()

        self.__pos[0] += dx
        self.__pos[1] -= dy

        self.__rect.x = int(self.__pos[0])
        self.__rect.y = int(self.__pos[1])

    def __die(self):
        self.kill()
        self.__living = False
        del self

    def get_properties(self):
        prop_dict = {}
        for attr in vars(self):
            if attr[:8] == "_Robot__":
                value = getattr(self, attr)
                if isinstance(value, (np.ndarray, list, dict)):
                    prop_dict[attr[8:]] = value.copy()
                else:
                    prop_dict[attr[8:]] = value
        return prop_dict

    def claim_coin(self, coin):
        self.__get_experience(coin.value)

    def flip_x(self):
        """
        flips the direction the robot is looking to.
        :return:
        """
        self.__turn_left = not self.__turn_left
        self.set_up()

    def set_up(self):
        """
        initializes the attributes for the sprite.
        :return:
        """
        image = pygame.image.load(self.__image_path).convert_alpha()
        self.__image = pygame.transform.scale(image, (self.__width, self.__height))
        if self.__turn_left:
            self.__image = pygame.transform.flip(self.__image, True, False)
        self.__rect = self.__image.get_rect()
        self.__rect.x, self.__rect.y = self.__pos[0],  self.__pos[1]

    def suffer(self, damage):
        """
        the robot takes damage.

        :param damage: float, positive
        :return:
        """
        if damage < 0:
            raise ValueError("damage must be non-negative, but {:} was obtained".format(damage))
        net_damage = damage * (1 - self.__armor / (self.__armor + 100))
        if self.__health <= net_damage:
            self.__health = 0
            self.__die()
        else:
            self.__health -= net_damage

    def distance(self, other):
        """
        computes the distance between the robot and other object (must have pos, width and height)
        :param other:
        :return:
        """
        return np.linalg.norm(other.pos + np.array([other.width, other.height]) / 2
                              - self.__pos - np.array([self.__width, self.__height]) / 2)

    def upgrade_stat(self, stat_key):
        """
        upgrades the stat denoted by the stat_key.
        :param stat_key: string
        :return:
        """
        if self.__experience_points <= 0:
            return
        else:
            self.__experience_points -= 1
            if stat_key == "damage":
                self.__damage += self.__g_damage * (0.65 + 0.035 * self.__level)
            elif stat_key == "max_health":
                self.__max_health += self.__g_max_health * (0.65 + 0.035 * self.__level)
            elif stat_key == "armor":
                self.__armor += self.__g_armor * (0.65 + 0.035 * self.__level)
            elif stat_key == "health_regen":
                self.__health_regen += self.__g_health_regen * (0.65 + 0.035 * self.__level)
            elif stat_key == "projectile_initial_speed":
                increase = (self.__max_projectile_initial_speed - self.__base_projectile_initial_speed) / 8
                if self.__max_projectile_initial_speed - self.__projectile_initial_speed - increase >= 0:
                    self.__projectile_initial_speed += increase
                elif self.__max_projectile_initial_speed - self.__projectile_initial_speed > 0:
                    self.__projectile_initial_speed = self.__max_projectile_initial_speed
                else:
                    self.__experience_points += 1
            elif stat_key == "projectile_per_second":
                self.__projectile_per_second += self.__g_projectile_per_second * (0.65 + 0.035 * self.__level)
            elif stat_key == "self_speed":
                increase = (self.__max_self_speed - self.__base_self_speed) / 8
                if self.__max_self_speed - self.__self_speed - increase >= 0:
                    self.__self_speed += increase
                elif self.__max_self_speed - self.__self_speed > 0:
                    self.__self_speed = self.__max_self_speed
                else:
                    self.__experience_points += 1
            else:
                self.__experience_points += 1

    def set_velocity(self, vx=None, vy=None):
        """
        sets the velocity of the robot.
        :param vx: float or None
        :param vy: float or None
        :return:
        """

        if vx is not None:
            self.__velocity[0] = np.clip(vx, - self.__self_speed, self.__self_speed)
        if vy is not None:
            self.__velocity[1] = np.clip(vy, - self.__self_speed, self.__self_speed)
        return self.__velocity

    def stop(self, direction='all'):
        """
        stops the robot in the given direction.
        :param direction: one of 'all', 'up', 'down', 'right', 'left'
        :return:
        """
        allowed_directions = ['all', 'up', 'down', 'right', 'left']
        if direction not in allowed_directions:
            raise Exception("Direction %s not allowed. It has to be one of " % direction + allowed_directions + '.')
        elif direction != 'all':
            self.__direction_move[direction] = True
            if direction in ['up', 'down']:
                self.__velocity[1] = 0.0
            else:
                self.__velocity[0] = 0.0
        else:
            for k in self.__direction_move.keys():
                self.__direction_move[k] = True
            self.__set_velocity(0, 0)

    def cast_basic_attack(self, target_position):
        """
        cast a basic attack if possible.
        :param target_position:
        :return:
        """
        if self.__time_since_attack < 1 / self.__projectile_per_second:
            return None

        if target_position[0] < self.__pos[0]:
            if not self.__turn_left:
                self.flip_x()
        elif self.__turn_left:
            self.flip_x()

        projectile_size = 8
        canon_x = self.__rect.x + (self.__rect.width + 1) * int(not self.__turn_left) - (projectile_size+1) * int(self.__turn_left)
        canon_y = self.__rect.y + self.__rect.height / 2
        projectile = Projectile(canon_x,
                                canon_y,
                                damage=self.__damage,
                                tx=target_position[0],
                                ty=target_position[1],
                                color=self.__projectile_color,
                                size=(projectile_size, projectile_size),
                                speed=self.__projectile_initial_speed)
        self.__time_since_attack = 0
        return projectile

    def update_image(self, image_path):
        self.__image_path = image_path
        self.set_up()

    def update(self, combat):
        """
        updates the robot object (natural healing, inner time and movement).
        :param combat: Combat object
        :return:
        """
        self.__heal(self.__health_regen / 60 / 5)
        self.__time_since_attack += 1/60
        self.move(combat=combat)
