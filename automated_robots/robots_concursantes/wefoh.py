import pygame
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np

class Wefoh(AutomatedRobot):

    def __init__(self, x, y, turn_left=False, **kwargs):
        kwargs["image_path"] = "Resources/wefoh.jpeg"
        AutomatedRobot.__init__(self, x, y, turn_left, **kwargs)

    def decide(self, other_robot_properties, coins, projectiles):
        """"Returns a projectile object or None."""

        self.other_robot_properties = other_robot_properties

        # Randomly decide what to upgrade
        if self.projectile_initial_speed < 5:
            self.upgrade_stat(self.stat_keys[1])
        elif self.self_speed < 5:
            self.upgrade_stat(self.stat_keys[3])
        elif self.armor < 200:
            self.upgrade_stat(self.stat_keys[4])
        else:
            self.upgrade_stat(self.stat_keys[2])

        move_vector, enemy_coin, distance_to_coin = self.check_coins(coins)

        # Randomly decide where to move
        for projectile in projectiles:
            if projectile.pos[0] > (self.pos[0] + self.width) and projectile.velocity[0] > 0:
                continue
            elif projectile.pos[0] < self.pos[0] and projectile.velocity[0] < 0:
                continue

            distance_vector = self.pos - projectile.pos
            distance = np.sqrt(distance_vector[0]**2 + distance_vector[1]**2)

            p_speed = np.sqrt(projectile.velocity[0]**2 + projectile.velocity[1]**2)

            if 150 > abs(distance) + 5*p_speed - self.max_self_speed*5:                
                move_vector = [projectile.velocity[0], projectile.velocity[1]]
                
                if self.pos[0] > 1000:
                    move_vector[0] = -abs(move_vector[0])
                elif self.pos[0] < 50:
                    move_vector[0] = abs(move_vector[0])
                
                if self.pos[1] > 700:
                    move_vector[1] = -abs(move_vector[1])
                elif self.pos[1] < 50:
                    move_vector[1] = abs(move_vector[1])

        vx,vy = move_vector[0], -move_vector[1]

        self.set_velocity(vy=vy,vx=vx)
        
        # Decide to cast a basic attack
        enemy_pos = other_robot_properties["pos"]
        enemy_pos[0] = enemy_pos[0] + self.width/2
        enemy_pos[1] = enemy_pos[1] + self.height/2
        distance_to_enemy = self.pos - enemy_pos

        distance_to_enemy = np.sqrt(distance_to_enemy[0]**2 + distance_to_enemy[1]**2)

        distance_enemy_to_coin = enemy_pos - enemy_coin
        distance_enemy_to_coin = np.sqrt(distance_enemy_to_coin[0]**2 + distance_enemy_to_coin[1]**2)

        if distance_to_coin > distance_to_enemy:
            bullet = self.cast_basic_attack(enemy_pos)
        elif distance_to_enemy < distance_enemy_to_coin:
            bullet = self.cast_basic_attack(enemy_pos)
        else:
            bullet = self.cast_basic_attack(enemy_coin)

        return bullet

    def check_coins(self, coins):
        min_dist = 100000
        enemy_min_dist = 100000
        move_vector = np.zeros((2,), dtype=int)
        pos = [self.pos[0] + self.width/2, self.pos[1] + self.height/2]
        enemy_coin_pos = [0,0]
        distance = 100000

        for coin in coins:
            distance_vector = coin.pos - pos
            enemy_distance_vector = coin.pos - self.other_robot_properties["pos"]
            
            distance = np.sqrt(distance_vector[0]**2 + distance_vector[1]**2)
            enemy_distance = np.sqrt(enemy_distance_vector[0]**2 + enemy_distance_vector[1]**2)
            
            if enemy_distance < enemy_min_dist:
                enemy_min_dist = enemy_distance
                enemy_coin_pos = coin.pos

            if enemy_distance < distance:
                continue

            if distance < min_dist:
                min_dist = distance
                move_vector = distance_vector

        return move_vector, enemy_coin_pos, distance