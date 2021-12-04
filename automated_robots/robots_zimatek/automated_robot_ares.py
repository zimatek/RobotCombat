from automated_robots.robots_zimatek.automated_robot_smartmove import SmartMoveRobot
from numpy import random
import numpy as np


class AresRobot(SmartMoveRobot):

    def decide_upgrade(self, **kwargs):
        if self.projectile_initial_speed <= self.self_speed:
            self.upgrade_stat("projectile_initial_speed")
        if self.self_speed < self.max_self_speed:
            self.upgrade_stat("self_speed")

        if np.random.random() < 0.7:
            self.upgrade_stat("damage")
        if np.random.random() < 0.5:
            self.upgrade_stat("projectile_per_second")
        if np.random.random() < 0.5:
            self.upgrade_stat("armor")

        up_choice = random.choice(self.stat_keys, size=4)
        for stat_up in up_choice:
            self.upgrade_stat(stat_up)