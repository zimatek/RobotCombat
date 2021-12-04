import pygame
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np


class MEGATRONCO(AutomatedRobot):

    def __init__(self, x, y, turn_left=False, **kwargs):
        kwargs["image_path"] = "Resources/MEGATRONCO.png"
        AutomatedRobot.__init__(self, x, y, turn_left, **kwargs)

    def decide(self,  other_robot_properties, coins, projectiles):
        """"Returns a projectile object or None."""
        up_list1 = ['self_speed', 'self_speed', 'self_speed', 'health_regen','health_regen', 'health_regen', 'max_health', 'armor', 'damage', 'projectil_initial_speed', 'projectile_per_second']
        self.upgrade_stat(up_list1[self.level-1])
        up_list2 = ['self_speed', 'self_speed', 'self_speed', 'health_regen','health_regen', 'health_regen', 'armor', 'armor', 'damage', 'projectile_per_second', 'projectile_per_second']
        self.upgrade_stat(up_list2[self.level-1])
        up_list3 = ['self_speed', 'self_speed', 'self_speed', 'health_regen','max_health', 'max_health', 'armor', 'armor', 'armor', 'projectile_per_second', 'projectil_initial_speed']
        self.upgrade_stat(up_list3[self.level-1])
        # up_list1 = ['self_speed', 'armor', 'health_regen', 'armor','self_speed', 'damage', 'armor', 'projectile_per_second', 'max_health', 'armor', 'damage']
        # self.upgrade_stat(up_list1[self.level-1])
        # up_list2 = ['self_speed', 'self_speed', 'self_speed', 'damage','projectil_initial_speed', 'damage', 'health_regen', 'projectil_initial_speed', 'max_health', 'damage', 'projectile_per_second']
        # self.upgrade_stat(up_list2[self.level-1])
        # up_list3 = ['self_speed', 'self_speed', 'self_speed', 'projectile_per_second','health_regen', 'damage', 'max_health', 'projectile_per_second', 'max_health', 'projectil_initial_speed', 'armor']
        # self.upgrade_stat(up_list3[self.level-1])
        
        
        self.upgrade_stat('self_speed')
        self.upgrade_stat('health_regen')

        self.upgrade_stat('max_health')
        self.upgrade_stat('armor')
        self.upgrade_stat('damage')
        self.upgrade_stat('projectile_per_second')
        self.upgrade_stat('projectil_initial_speed')
        
        # self.upgrade_stat('self_speed')
        # self.upgrade_stat('self_speed')
        # self.upgrade_stat('self_speed')
        # self.upgrade_stat('max_health')
        # self.upgrade_stat('health_regen')
        # self.upgrade_stat('armor')
        # self.upgrade_stat('damage')
        # self.upgrade_stat('projectile_per_second')
        # self.upgrade_stat('self_speed')
        
                          
        coin_positions = np.asarray([coin.pos for coin in coins])
        coin_distances = np.asarray([np.linalg.norm(pos-self.pos) for pos in coin_positions])
        if coin_distances.size != 0:
            close_arg = np.argmin(coin_distances)
            r_min = coin_positions[close_arg]-self.pos
            #print(r_min)
            self.set_velocity(r_min[0], -r_min[1])
            
            
        return self.cast_basic_attack(other_robot_properties['pos'])

        