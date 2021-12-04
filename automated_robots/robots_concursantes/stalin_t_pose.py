# -*- coding: utf-8 -*-
import pygame
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np
import math


class stalin_t_pose(AutomatedRobot):
    
    def get_distance_to_pos(self, px, py):
        distance = math.sqrt((self.pos[0] + self.width/2 - px)**2 + (self.pos[1] + self.height/2 - py)**2)
        return distance
    
    def get_distance_betwing(self, px, py, p2x, p2y):
        distance = math.sqrt((p2x - px)**2 + (p2y - py)**2)
        return distance

    def decide(self, other_robot_properties, coins, projectiles):
        """"Returns a projectile object or None."""
        # Randomly decide what to upgrade
        number_of_speed = 3
        #print(self.armor)
        #print(self.health_regen)
        if self.self_speed < 4.5:
            self.upgrade_stat("self_speed")
        elif self.health_regen < 23:
            self.upgrade_stat("health_regen")
        else:
            self.upgrade_stat("armor")
        
        #print(self.health)
        avoiding = False
        if self.health < 400:        
            avoiding = True
        
        
        
        coins_list = []
        for coin in coins:
            coins_list.append(coin)
        vx = 0
        vy = 0
        
        pos_x_center = self.pos[0] + self.width/2
        pos_y_center = self.pos[1] + self.height/2
        
        other_x_center = other_robot_properties["pos"][0] + self.width/2
        other_y_center = other_robot_properties["pos"][1] + self.height/2

        if avoiding:
            for coin in coins_list:
                dist = self.get_distance_betwing(coin.pos[0], coin.pos[1], other_x_center, other_y_center)
                if dist < 300:
                    coins_list.remove(coin)
        
        if len(coins_list) != 0:            
            distances = np.empty(len(coins_list))
            for i, coin in enumerate(coins_list):
                distances[i] = self.get_distance_to_pos(coin.pos[0], coin.pos[1])
            
            near_coin_index = np.argmin(distances)
            near_coin = coins_list[near_coin_index]
            vx_nor = (near_coin.pos[0] - pos_x_center) / self.get_distance_to_pos(coin.pos[0], coin.pos[1])
            vy_nor = (near_coin.pos[1] - pos_y_center) / self.get_distance_to_pos(coin.pos[0], coin.pos[1])
            
            v_max = max(abs(vx_nor), abs(vy_nor))
            rate = self.self_speed / v_max
            
            vx = vx_nor * rate
            vy = vy_nor * rate
        
        
        # if avoiding:
        #     projectiles_list = []
        #     for projectil in projectiles:
        #         projectiles_list.append(projectil)
            
        #     for projectil in projectiles_list:
                
        #         next_pos_x = projectil.pos[0] + 30*projectil.velocity[0]
        #         next_pos_y = projectil.pos[1] + 30*projectil.velocity[1]
                
        #         colition_width = 30
                
        #         if (next_pos_x < self.pos[0] + self.width/2 + colition_width and next_pos_x > self.pos[0] - colition_width):
        #             if(next_pos_y < self.pos[1] + self.height/2 + colition_width and next_pos_y > self.pos[1] - colition_width):
        #                 print("peligro")
                        
        #                 vx_nor = projectil.velocity[1]
        #                 vy_nor = -projectil.velocity[0]
                        
        #                 v_max = max(abs(vx_nor), abs(vy_nor))
        #                 rate = self.self_speed / v_max
                        
        #                 vx = vx_nor * rate
        #                 vy = vy_nor * rate
            
        
        self.set_velocity(vx=vx, vy=-vy)

## Tiroaren balioa
        enemy_moveing_to_coin = False
        if(not enemy_moveing_to_coin):
            target_pos = [0, 0]
            
            if len(coins_list) != 0:            
                distances = np.empty(len(coins_list))
                for i, coin in enumerate(coins_list):
                    distances[i] = self.get_distance_betwing(coin.pos[0], coin.pos[1], other_x_center, other_y_center)
                
                near_coin_index = np.argmin(distances)
                near_coin = coins_list[near_coin_index]
                
                target_pos[0] = near_coin.pos[0]
                target_pos[1] = near_coin.pos[1]


            other_rob_pos = other_robot_properties['pos']
            other_rob_vel = other_robot_properties['velocity']
            
            my_rob_pos = self.pos
            my_rob_shoot_speed = self.projectile_initial_speed
            
            rel_rob_pos = [0,0]
            
            for i in range(1):
                rel_rob_pos[i] = other_rob_pos[i] - my_rob_pos[i]
    
            mod_rel_pos =  math.sqrt(abs(rel_rob_pos[0])* abs(rel_rob_pos[0]) +  abs(rel_rob_pos[1])* abs(rel_rob_pos[1]))
            
            # CORRECCION DE TIRO
                
            if mod_rel_pos<150:
                target_pos = np.array([other_rob_pos[0],other_rob_pos[1]])
    
    
            return self.cast_basic_attack(target_pos)
                
        else:
            return None





