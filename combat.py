import pygame
from robot import Robot
from manual_robot import ManualRobot
from automated_robot import AutomatedRobot
from automated_robots.automated_robot_idle import IdleRobot
from automated_robots.automated_robot_random import RandomRobot
# Here you should import the your AutomatedRobot
from robot_hub import RobotHub
from coin import Coin
import numpy as np
import os


class Combat:
    """
    A class to represent a robot combat environment.

    ...

    Attributes
    ----------
    dims : list
        with and height of the screen, dims = [width, height]
    robots : pygame.sprite.Group
        a sprite group containing the robot objects
    robot_list : list
        a list containing the robot objects
    left_robot : Robot
        the Robot that starts in the left-hand side
    right_robot : Robot
        the Robot that starts in the right-hand side
    robot_hubs : pygame.sprite.Group
        a sprite group containing the RobotHub objects
    coin_per_second : float
        estimated coin per second

    Methods
    -------
    fix_bugs:
        fixes bugs in the position of the robot sprites
    run:
        runs the robot combat

    """

    def __init__(self, left_robot: Robot, right_robot: Robot, coin_per_second: float):
        self.dims = (1050, 750)

        self.robots = pygame.sprite.Group()
        self.robots.add(left_robot)
        self.robots.add(right_robot)
        self.robot_list = [left_robot, right_robot]
        self.left_robot = left_robot
        self.right_robot = right_robot

        self.robot_hubs = pygame.sprite.Group()
        self.left_robot_hub = RobotHub(self.left_robot, RobotHub.DownLeft)
        self.right_robot_hub = RobotHub(self.right_robot, RobotHub.DownRight)

        self.robot_hubs.add(self.left_robot_hub)
        self.robot_hubs.add(self.right_robot_hub)

        self.coin_per_second = coin_per_second

        self.font = None
        self.font2 = None

    def fix_bugs(self):
        """
        fixes bugs in the position of the robot sprites

        :return:
        """
        if self.right_robot.living and self.left_robot.living:
            collide = self.left_robot.rect.colliderect(self.right_robot.rect)
            if collide:
                if self.left_robot.rect.x <= self.right_robot.rect.x:
                    self.left_robot.move(dx=-self.left_robot.rect.width, combat=self)
                    self.right_robot.move(dx=self.right_robot.rect.width, combat=self)
                else:
                    self.left_robot.move(dx=self.left_robot.rect.width, combat=self)
                    self.right_robot.move(dx=-self.right_robot.rect.width, combat=self)

    def run(self):
        """
        runs the robot combat

        :return:
        """
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("Resources/Pokemon_Classic.ttf", 16)
        self.font2 = pygame.font.Font("Resources/Pokemon_Classic.ttf", 28)

        background_image = pygame.image.load("Resources/background_mountains.jpg")
        background_image = pygame.transform.rotozoom(background_image, 0, 2.5)
        os.environ['SDL_VIDEO_CENTERED'] = '0'
        screen = pygame.display.set_mode(self.dims)
        pygame.display.set_caption("Robot Combat: {:s} vs {:s}".format(str(type(self.left_robot)).split(".")[-1][:-2],
                                                                       str(type(self.right_robot)).split(".")[-1][:-2]))

        for robot in self.robots:
            robot.set_up()

        for hub in self.robot_hubs:
            hub.set_up()

        # PRE LOOP
        sprites_all = pygame.sprite.Group()
        projectiles = pygame.sprite.Group()
        coins = pygame.sprite.Group()
        stop = False
        pause = False
        winner = None

        sprites_all.add(self.robots)
        sprites_all.add(projectiles)
        sprites_all.add(coins)
        clock = pygame.time.Clock()

        time = 1
        count_down = 60*3
        totalcoins = 0

        # -------- Principal Loop of the Program -----------
        while not stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                    if event.key == pygame.K_1:
                        pause = True
                        winner = 1
                    if event.key == pygame.K_0:
                        pause = True
                        winner = 0

                if isinstance(self.left_robot, ManualRobot) and self.left_robot.living:
                    projectile = self.left_robot.decide(event, self.left_robot_hub)
                    if projectile is not None:
                        sprites_all.add(projectile)
                        projectiles.add(projectile)

                elif isinstance(self.right_robot, ManualRobot) and self.right_robot.living:
                    projectile = self.right_robot.decide(event, self.right_robot_hub)
                    if projectile is not None:
                        sprites_all.add(projectile)
                        projectiles.add(projectile)

            # --- The Logic
            if not pause:
                np.random.shuffle(self.robot_list)
                for robot in self.robot_list:
                    if robot == self.left_robot:
                        other = self.right_robot
                    else:
                        other = self.left_robot
                    if isinstance(robot, AutomatedRobot) and robot.living:
                        projectile = robot.decide(other_robot_properties=other.get_properties(),
                                                  coins=coins,
                                                  projectiles=projectiles)
                        if projectile is not None:
                            sprites_all.add(projectile)
                            projectiles.add(projectile)

                for robot in self.robot_list:
                    if robot.living:
                        robot_damaged = pygame.sprite.spritecollide(robot, projectiles, True)
                        coins_captured = pygame.sprite.spritecollide(robot, coins, True)

                        for projectile_hit in robot_damaged:
                            robot.suffer(projectile_hit.damage)
                        for coin in coins_captured:
                            robot.claim_coin(coin)
                        robot.update(combat=self)

                for projectile in projectiles:
                    projectile.draw(screen)
                    projectile.update(combat=self)

                coins.update()

                self.fix_bugs()

                if np.random.random() < self.coin_per_second / 60:
                    totalcoins += 2
                    pos1 = 50 + np.random.random(2) * (np.array(self.dims)-100) * np.array([0.5, 1])
                    pos2 = np.array(self.dims) * np.array([1, 0]) + pos1 * np.array([-1, 1])
                    coin_left = Coin(pos1)
                    coin_right = Coin(pos2)
                    coins.add(coin_left)
                    coins.add(coin_right)
                    sprites_all.add(coin_left)
                    sprites_all.add(coin_right)

            # --- The image
            screen.fill((255, 255, 255))
            screen.blit(background_image, (0, 0))
            sprites_all.draw(screen)

            for projectile in projectiles:
                projectile.draw(screen)

            for hub in self.robot_hubs:
                hub.draw(screen)

            time_text = self.font.render("{:02d}:{:02d}".format(int((time / 60) // 60), int((time / 60) % 60)), False,
                                         (0, 0, 0))
            screen.blit(time_text, (self.dims[0] - 5 - time_text.get_width(), 5))

            coin_text = self.font.render("# {:d}/{:d}".format(len(coins), int(totalcoins)), False,
                                         (0, 0, 0))
            screen.blit(coin_text, (self.dims[0] - 5 - coin_text.get_width(), 5 + coin_text.get_height()))

            if self.left_robot.living and not self.right_robot.living:
                winner = 1
                pause = True
            if not self.left_robot.living and self.right_robot.living:
                winner = 0
                pause = True

            if pause:
                if winner == 1:
                    pause_text = self.font2.render(
                        "The winner is {:s}".format(str(type(self.left_robot)).split(".")[-1][:-2]), False, (0, 0, 0))
                    center = (self.dims[0] // 2, self.dims[1] // 2)
                    text_rect = pause_text.get_rect(center=center)
                    screen.blit(pause_text, text_rect)
                elif winner == 0:
                    pause_text = self.font2.render(
                        "The winner is {:s}".format(str(type(self.right_robot)).split(".")[-1][:-2]), False, (0, 0, 0))
                    center = (self.dims[0] // 2, self.dims[1] // 2)
                    text_rect = pause_text.get_rect(center=center)
                    screen.blit(pause_text, text_rect)
                else:
                    pause_text = self.font.render("Paused", False, (0, 0, 0))
                    center = (self.dims[0] // 2, self.dims[1] // 2)
                    text_rect = pause_text.get_rect(center=center)
                    screen.blit(pause_text, text_rect)
            else:
                time += 1

            pygame.display.flip()

            clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    attributes = {
        "health": 500,
        "armor": 90,
        "health_regen": 19,
        "damage": 65,
        "self_speed": 3,
        "projectile_initial_speed": 4,
        "projectile_per_second": 0.6,
        "g_health": 80,
        "g_armor": 8,
        "g_health_regen": 2,
        "g_damage": 12,
        "g_projectile_per_second": 0.05,
        "max_self_speed": 5,
        "max_projectile_initial_speed": 10,
        "experience_for_level_up": 7,
        "g_experience_for_level_up": 3
    }

    cps = 2

    bots = pygame.sprite.Group()
    bot1 = ManualRobot(x=150, y=325, **attributes)
    bot2 = RandomRobot(x=1050-150-4*32, y=325, turn_left=True,
                      projectile_color=(38, 162, 149), image_path="Resources/simple_robot_green.png",
                      **attributes)
    mg = Combat(bot1, bot2, coin_per_second=cps)
    mg.run()
