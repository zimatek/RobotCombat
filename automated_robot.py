from robot import Robot


class AutomatedRobot(Robot):
    """
        A Robot class for automated control.
    """

    def __init__(self, x, y, turn_left=False, **kwargs):
        Robot.__init__(self, x, y, turn_left, **kwargs)

    def decide(self, other_robot_properties, coins, projectiles):
        """
        Decides about movement, about upgrading stats and casting an attack.

        :param other_robot_properties: dictionary with the properties of the other robot
        :param coins: sprite group with the coins
        :param projectiles: sprite group with the projectiles
        :return: Projectile object or None
        """
        return None
