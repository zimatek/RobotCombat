import pygame
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np

import math

class Roby(AutomatedRobot):

    def decide(self, other_robot_properties, coins, projectiles):
        """"Returns a projectile object or None."""
        
        def goTo(vec):
            x, y = vec[0], vec[1]
            d = math.sqrt((self.pos[0]-x)**2 + (self.pos[1]-y)**2)
            if d < 10:
                return True
            dx = self.pos[0]-x
            dy = self.pos[1]-y
            DX, DY = 0, 0
            p = True
            v = self.max_self_speed
            while 2*v > 0:
                if p and abs(dx) > 2:
                    DX -= dx/abs(dx)
                elif abs(dy) > 2:
                    DY += dy/abs(dy)
                v -= 1
                if p:
                    p = False
                else:
                    p = True
            self.set_velocity(DX, DY)
            return False

        def distance(pos1, pos2):
            return max(abs(pos1[0]-pos2[0]), abs(pos1[1]-pos2[1]))


        #################
        #buscar monedas
        if self.level < 10:
            coinList = []
            self.closestCoinPos = (0,0)
            minDistance = None
            for coin in coins:
                coinPos = coin.pos
                if minDistance == None or distance(self.pos, coinPos) < minDistance:
                    minDistance = distance(self.pos, coinPos)
                    self.closestCoinPos = coinPos
            goTo(self.closestCoinPos)
        else:
            goTo(other_robot_properties['pos'])
        #mejoras
        for _ in range(10):
            self.upgrade_stat('self_speed')
        for _ in range(50):
            if self.max_health < 1100:
                self.upgrade_stat('max_health')
        for _ in range(50):
            self.upgrade_stat('damage')
            self.upgrade_stat('projectile_per_second')
        #disparar
        deltaX = (self.pos[0]-other_robot_properties['pos'][0])
        deltaY = (self.pos[1]-other_robot_properties['pos'][1])
        if abs(deltaX/math.sqrt(deltaX**2 + deltaY**2)) > 0.35:
            return self.cast_basic_attack(other_robot_properties['pos'])
        return None