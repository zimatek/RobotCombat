import pygame
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np


class IdleRobot(AutomatedRobot):

    def decide(self, **kwargs):
        """"Returns a projectile object or None."""
        # Just... do nothing
        return None
