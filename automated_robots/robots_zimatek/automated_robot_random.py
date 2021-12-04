from automated_robot import AutomatedRobot
from numpy import random
import numpy as np


class RandomRobot(AutomatedRobot):

    def decide(self,  other_robot_properties, coins, projectiles):
        """"Returns a projectile object or None."""

        # Randomly decide what to upgrade
        ii = random.randint(len(self.stat_keys), size=3)
        for i in ii:
            self.upgrade_stat(self.stat_keys[i])

        # Randomly decide where to move
        up_down_none = random.randint(3)
        key = random.randint(4)

        if up_down_none == 0:
            if key == 0:
                self.set_velocity(vy=10)
            if key == 1:
                self.set_velocity(vy=-10)
            if key == 2:
                self.set_velocity(vx=10)
            if key == 3:
                self.set_velocity(vx=-10)
        elif up_down_none == 1:
            if key == 0:
                self.stop('up')
            if key == 1:
                self.stop('down')
            if key == 2:
                self.stop('right')
            if key == 3:
                self.stop('left')

        # Decide to cast a basic attack
        cast = random.randint(2)
        if cast == 0:
            pos = random.random(2) * np.array([1000, 10000])
            if pos[0] < self.rect.x - 100 or pos[0] > self.rect.x + self.rect.width + 100:
                if pos[1] < self.rect.y - 100 or pos[1] > self.rect.y + self.rect.height + 100:
                    return self.cast_basic_attack(pos)
        else:
            return None
