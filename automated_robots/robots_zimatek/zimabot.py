import pygame
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np


class Zimabot(AutomatedRobot):

    def __init__(self, x, y, turn_left=False, **kwargs):
        kwargs["image_path"] = "Resources/zimabot/zimabot_2.png"
        AutomatedRobot.__init__(self, x, y, turn_left, **kwargs)
        self.__inner_time = 0
        self.__angry_time = 0
        self.__attack_time = 0
        self.__angry = False
        self.__destroyer = False
        self.__prev_health = self.health

    def decide_upgrade(self, **kwargs):
        if self.projectile_initial_speed <= self.self_speed * np.sqrt(2):
            self.upgrade_stat("projectile_initial_speed")
        if self.self_speed < self.max_self_speed:
            self.upgrade_stat("self_speed")

        if self.max_health < 600:
            if np.random.random() < 0.75:
                self.upgrade_stat("max_health")
            if np.random.random() < 0.5:
                self.upgrade_stat("health_regen")
            if np.random.random() < 0.5:
                self.upgrade_stat("armor")
        else:
            if np.random.random() < 0.75:
                self.upgrade_stat("damage")
                self.upgrade_stat("projectile_per_second")
            if np.random.random() < 0.75:
                self.upgrade_stat("max_health")
            if np.random.random() < 0.5:
                self.upgrade_stat("health_regen")
            if np.random.random() < 0.5:
                self.upgrade_stat("armor")

        up_choice = random.choice(self.stat_keys, size=4)
        for stat_up in up_choice:
            self.upgrade_stat(stat_up)

    def decide_cast_attack(self, other_robot_properties):
        if other_robot_properties["living"]:
            pos = other_robot_properties["pos"] + np.array([other_robot_properties["width"]/2, other_robot_properties["height"]/2])
            if pos[0] < self.rect.x - 50 or pos[0] > self.rect.x + self.rect.width + 50:
                return self.cast_basic_attack(pos)
        else:
            return None

    def move_to_coin(self, **kwargs):
        coins = kwargs["coins"]
        distance = 100 * self.width
        nearest_coin = None
        # for coin in coins:
        #     dist = self.distance(coin)
        #     if dist < distance:
        #         distance = dist
        #         nearest_coin = coin

        if len(coins) > 0:
            center_of_mas = np.average(np.array([coin.pos for coin in coins]),
                                       weights=np.array([1/(1+self.distance(coin))**2 for coin in coins]), axis=0)
            for coin in coins:
             dist = np.linalg.norm(coin.pos - center_of_mas)
             if dist < distance:
                 distance = dist
                 nearest_coin = coin

        if nearest_coin is not None:
            dx, dy = 10 * (nearest_coin.pos - self.pos - np.array([self.width / 2, self.height / 2]))
        else:
            dx, dy = (0, 0)
        self.set_velocity(dx, -dy)
        return nearest_coin

    def dodge(self, **kwargs):
        projectiles = kwargs["projectiles"]
        near = 350
        distance = 100 * self.width
        danger_projectile = None
        for projectile in projectiles:
            dist = np.linalg.norm(projectile.pos - self.pos)
            dist2 = np.linalg.norm(projectile.pos + projectile.velocity - self.pos - self.velocity)
            if dist2 < near and dist2 < dist and dist2 < distance:
                distance = dist2
                danger_projectile = projectile

        if danger_projectile is not None:
            dx, dy = 10 * projectile.velocity

            if self.pos[1] < self.height:
                if dx > 0:
                    self.set_velocity(-dy, dx)
                else:
                    self.set_velocity(dy, -dx)
            else:
                if dx > 0:
                    self.set_velocity(dy, -dx)
                else:
                    self.set_velocity(-dy, dx)

    def decide(self, other_robot_properties, coins, projectiles):
        """"Returns a projectile object or None."""

        # Blink
        self.__inner_time += 1
        if self.__prev_health > self.health and self.health < 0.85 * self.max_health:
            self.__angry = True
            self.__destroyer = True
            self.__angry_time = self.__inner_time
        elif self.__angry_time - self.__angry_time > 5:
            self.__angry = False
        self.__prev_health = self.health

        if self.__attack_time > 2 or not self.__destroyer:
            self.__attack_time += 1
            if not self.__angry:
                if self.__inner_time % 30 < 25:
                    self.update_image("Resources/zimabot/zimabot_1.png")
                else:
                    self.update_image("Resources/zimabot/zimabot_7.png")
            else:
                self.update_image("Resources/zimabot/zimabot_4.png")
        if other_robot_properties["health"] <= self.damage * (1-other_robot_properties["armor"] / (100 + other_robot_properties["armor"])):
            self.update_image("Resources/zimabot/zimabot_3.png")
        if self.experience <= 4 and self.level >= 3:
            self.update_image("Resources/zimabot/zimabot_3.png")

        # Randomly decide what to upgrade
        self.decide_upgrade()

        # Move towards the nearest coin
        nearest_coin = self.move_to_coin(coins=coins)

        # Move away if a projectile is too near and moving towards me
        # Only if the robot has low health
        if self.health < 5 * other_robot_properties["damage"] or nearest_coin is None:
            self.dodge(projectiles=projectiles)

        # Decide to cast a basic attack
        if self.__destroyer:
            proj = self.decide_cast_attack(other_robot_properties)
            if proj is not None:
                if self.image_path == "Resources/zimabot/zimabot_6.png":
                    self.update_image("Resources/zimabot/zimabot_5.png")
                else:
                    self.update_image("Resources/zimabot/zimabot_6.png")
                self.__attack_time = 0
                return proj
