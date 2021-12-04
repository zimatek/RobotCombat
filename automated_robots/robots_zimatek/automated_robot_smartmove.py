import pygame
from robot import Robot
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np


class SmartMoveRobot(AutomatedRobot):

    def decide_upgrade(self):
        if self.projectile_initial_speed <= self.self_speed:
            self.upgrade_stat("projectile_initial_speed")
        if self.self_speed < self.max_self_speed:
            self.upgrade_stat("self_speed")
        up_choice = random.choice(self.stat_keys, size=4)
        for stat_up in up_choice:
            self.upgrade_stat(stat_up)

    def decide_cast_attack(self, other_robot_properties):
        if other_robot_properties["living"]:
            cast = random.random()
            if cast < 0.75:
                pos = other_robot_properties["pos"] + np.array([other_robot_properties["width"]/2, other_robot_properties["height"]/2])
                if pos[0] < self.rect.x - 50 or pos[0] > self.rect.x + self.rect.width + 50:
                    return self.cast_basic_attack(pos)
            else:
                return None
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

        # Randomly decide what to upgrade
        self.decide_upgrade()

        # Move towards the nearest coin
        nearest_coin = self.move_to_coin(coins=coins)

        # Move away if a projectile is too near and moving towards me
        # Only if the robot has low health
        if self.health < 5 * other_robot_properties["damage"] or nearest_coin is None:
            self.dodge(projectiles=projectiles)

        # Decide to cast a basic attack
        return self.decide_cast_attack(other_robot_properties)
