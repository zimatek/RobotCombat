import pygame
from robot import Robot


class ManualRobot(Robot):
    """
        A Robot class for manual control.
    """

    def __init__(self, x, y, turn_left=False, **kwargs):
        Robot.__init__(self, x, y, turn_left, **kwargs)

    def decide(self, event, robot_hub):
        """
        Makes a decision for movement, stats and casting attacks, according to the event and robot_hub information.

        :param event: pygame event object
        :param robot_hub: RobotHub object
        :return: Projectile or None
        """
        hub_activated = robot_hub.get_event(event, pygame.mouse)

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.set_velocity(vy=10)
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                self.set_velocity(vy=-10)
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.set_velocity(vx=10)
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                self.set_velocity(vx=-10)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.stop('up')
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                self.stop('down')
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.stop('right')
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                self.stop('left')

        if event.type == pygame.MOUSEBUTTONUP and not hub_activated:
            pos = pygame.mouse.get_pos()
            return self.cast_basic_attack(pos)
        else:
            return None
