import pygame
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np

class Piton_3(AutomatedRobot):

    def __init__(self, x, y, turn_left=False, **kwargs):
        kwargs["image_path"] = "Resources/roombabuena.png"
        AutomatedRobot.__init__(self, x, y, turn_left, **kwargs)

    def decide(self,  other_robot_properties, coins, projectiles):
        
        posr = self.pos
        x = posr[0]
        y = posr[1]
        cercanas = []
        
        v = self.self_speed
        if v < 5:
            self.upgrade_stat("self_speed")
            self.upgrade_stat("self_speed")
            self.upgrade_stat("self_speed")
        else:
            self.upgrade_stat("max_health")
            self.upgrade_stat("armor")
            self.upgrade_stat("health_regen")
        rmin = 100000
        for coin in coins:
            coin_pos = coin.pos
            xc = coin_pos[0]
            yc = coin_pos[1]
            r = np.sqrt((x-xc)**2+(y-yc)**2)
            cercanas.append([coin_pos,r])
        for p in cercanas:
            pos_moneda = p[0]
            if p[1] < rmin:
                p[1]=rmin
                xm = pos_moneda[0]
                ym = pos_moneda[1]
            
            if x < xm and y < ym:
                self.set_velocity(vx =10,vy =-10)
            elif x < xm and y > ym:
                self.set_velocity(vx =10,vy = 10)
            elif x > xm and y > ym:
                self.set_velocity(vx =-10,vy =10)
            elif  x > xm and y < ym:
                self.set_velocity(vx =-10,vy =-10)
                
        

                
                
        """"Returns a projectile object or None."""

        # Randomly decide what to upgrade
       


        # Decide to cast a basic attack
    
        
