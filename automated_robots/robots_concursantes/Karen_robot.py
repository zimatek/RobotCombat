import pygame
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np

def distances(pos_1, pos_2):
    return ((pos_1[0]-pos_2[0])**2 + (pos_1[1]-pos_2[1])**2)**(1/2)
class Karen(AutomatedRobot):

    def __init__(self, x, y, turn_left=False, **kwargs):
        kwargs["image_path"] = "Resources/Karen-blue-form-stock-art.png"
        AutomatedRobot.__init__(self, x, y, turn_left, **kwargs)

    def closest_coin(self, coins):
        a = None
        for i in coins:
            if a == None:
                a = distances(self.pos, i.pos)
                coin = i
            b = distances(self.pos, i.pos)
            if b < a:
                a = b
                coin = i
        return coin.pos
    def closest_projectile(self, projectiles):
        a = None
        for i in projectiles:
            if a == None:
                a = distances(self.pos, i.pos)
                projectile = i
            b = distances(self.pos, i.pos)
            if b < a:
                a = b
                projectile = i
        return (projectile.pos, projectile.velocity)
    def go_closest_coin(self, coins):
        a = self.closest_coin(coins) - self.pos
        if abs(a[0]) <= abs(a[1]):
            self.set_velocity(vy=self.self_speed*(a[1]/abs(a[1])))
            self.set_velocity(vx=self.self_speed*(abs(a[0])/abs(a[1]))*(a[0]/abs(a[0])))
        else:
            self.set_velocity(vx=self.self_speed*(a[0]/abs(a[0])))
            self.set_velocity(vy=self.self_speed*(abs(a[1])/abs(a[0]))*(a[1]/abs(a[1])))

    
    def decide(self,  other_robot_properties, coins, projectiles):
        ii = random.randint(len(self.stat_keys), size=56)
        if self.health <= self.max_health/4:
            self.update(health)
        for i in ii:
            self.upgrade_stat(self.stat_keys[i])
        if random.randint(3000000)%119==0:
            a=1
            if random.randint(100)%2==0:
                a=-1
            self.set_velocity(vy=a*self.self_speed)
        if coins:
            self.go_closest_coin(coins)
        return self.cast_basic_attack(other_robot_properties['pos'])
            
        
        
        



            
    
