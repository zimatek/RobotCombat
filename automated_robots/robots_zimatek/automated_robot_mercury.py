from automated_robots.robots_zimatek.automated_robot_smartmove import SmartMoveRobot
from numpy import random


class MercuryRobot(SmartMoveRobot):

    def decide_upgrade(self, **kwargs):
        if self.projectile_initial_speed <= self.self_speed:
            self.upgrade_stat("projectile_initial_speed")
        if self.self_speed < self.max_self_speed:
            for i in range(3):
                self.upgrade_stat("self_speed")
        if self.projectile_per_second < 2:
            self.upgrade_stat("projectile_per_second")
        up_choice = random.choice(self.stat_keys, size=4)
        for stat_up in up_choice:
            self.upgrade_stat(stat_up)
