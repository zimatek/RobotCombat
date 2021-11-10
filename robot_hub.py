import pygame
import numpy as np


class RobotHub(pygame.sprite.Sprite):
    """
    A class to handle the robot hub.
    """
    DownLeft = 0
    UpLeft = 1
    UpRight = 2
    DownRight = 3

    def __init__(self, robot, hub_position, screen_shape=[1050, 750]):
        pygame.sprite.Sprite.__init__(self)

        self.robot = robot
        self.hub_up = hub_position in [1, 2]
        self.hub_down = not self.hub_up
        self.hub_left = hub_position < 2
        self.hub_right = hub_position >= 2

        self.screen_width = screen_shape[0]
        self.screen_height = screen_shape[1]

        self.height = 100
        self.width = 250

        self.x = self.hub_right * (self.screen_width - self.width)
        self.y = self.hub_down * (self.screen_height - self.height)

        self.hub_grid = np.zeros((2, 4, 2))
        self.hub_grid[:, :, 0] = self.x + 12 + self.hub_right * 16 + 60 * np.arange(4)
        self.hub_grid[:, :, 1] = np.repeat(self.y + 42 + 24 * np.arange(2), 4, axis=0).reshape((2, 4))

        self.bg_color = (194, 203, 218)
        self.frame_color = (39, 43, 66)

        self.frame_body = None
        self.frame_corner = None
        self.sword = None

        self.font = None
        self.canon = None
        self.arch = None
        self.running = None
        self.heart = None
        self.plus = None
        self.shield = None

        self.buttons = {}

    def set_up(self):
        frame_body = pygame.image.load("Resources/robot_hub_body.png").convert_alpha()
        self.frame_body = pygame.transform.scale(frame_body, (self.width - self.height, self.height))
        self.frame_body = pygame.transform.flip(self.frame_body, self.hub_right, self.hub_up)

        frame_corner = pygame.image.load("Resources/robot_hub_corner.png").convert_alpha()
        self.frame_corner = pygame.transform.scale(frame_corner, (self.height, self.height))
        self.frame_corner = pygame.transform.flip(self.frame_corner, self.hub_right, self.hub_up)

        fontsize = 12
        self.sword = pygame.image.load("Resources/sword.png")
        self.canon = pygame.image.load("Resources/canon.png")
        self.arch = pygame.image.load("Resources/arch.png")
        self.running = pygame.image.load("Resources/running.png")
        self.shield = pygame.image.load("Resources/shield.png")
        self.heart = pygame.image.load("Resources/heart.png")
        self.plus = pygame.image.load("Resources/plus.png")

        self.font = pygame.font.Font("Resources/Pokemon_Classic.ttf", fontsize)

        self.buttons["damage"] = Button(self.hub_grid[0, 0]-2, (16+4, 16+4), False, bg=self.bg_color, frame=self.frame_color)
        self.buttons["projectile_initial_speed"] = Button(self.hub_grid[0, 1]-2, (16+4, 16+4), False, bg=self.bg_color, frame=self.frame_color)
        self.buttons["projectile_per_second"] = Button(self.hub_grid[0, 2]-2, (16+4, 16+4), False, bg=self.bg_color, frame=self.frame_color)
        self.buttons["self_speed"] = Button(self.hub_grid[0, 3]-2, (16+4, 16+4), False, bg=self.bg_color, frame=self.frame_color)
        self.buttons["armor"] = Button(self.hub_grid[1, 0]-2, (16+4, 16+4), False, bg=self.bg_color, frame=self.frame_color)
        self.buttons["max_health"] = Button(self.hub_grid[1, 1]-2, (16+4, 16+4), False, bg=self.bg_color, frame=self.frame_color)
        self.buttons["health_regen"] = Button(self.hub_grid[1, 2]-2, (16+4, 16+4), False, bg=self.bg_color, frame=self.frame_color)

    def __draw_frame(self, surface):
        surface.blit(self.frame_body, (self.x + self.hub_right * self.height,
                                       self.y))
        surface.blit(self.frame_corner, (self.x + self.hub_left * (self.width - self.height),
                                         self.y))

    def __draw_stats(self, surface):
        surface.blit(self.sword, self.hub_grid[0, 0])
        surface.blit(self.font.render("{:3d}".format(int(self.robot.damage)), False, (0, 0, 0)),
                     self.hub_grid[0, 0] + np.array([16, 0]))
        surface.blit(self.canon, self.hub_grid[0, 1])
        surface.blit(self.font.render("{:2d}".format(int(self.robot.projectile_initial_speed)), False, (0, 0, 0)),
                     self.hub_grid[0, 1] + np.array([16, 0]))
        surface.blit(self.arch, self.hub_grid[0, 2])
        surface.blit(self.font.render("{:3.1f}".format(self.robot.projectile_per_second), False, (0, 0, 0)),
                     self.hub_grid[0, 2] + np.array([16, 0]))
        surface.blit(self.running, self.hub_grid[0, 3])
        surface.blit(self.font.render("{:2.1f}".format(self.robot.self_speed), False, (0, 0, 0)),
                     self.hub_grid[0, 3] + np.array([16, 0]))

        surface.blit(self.shield, self.hub_grid[1, 0])
        surface.blit(self.font.render("{:3d}".format(int(self.robot.armor)), False, (0, 0, 0)),
                     self.hub_grid[1, 0] + np.array([16, 0]))
        surface.blit(self.heart, self.hub_grid[1, 1])
        surface.blit(self.font.render("{:3d}".format(int(self.robot.max_health)), False, (0, 0, 0)),
                     self.hub_grid[1, 1] + np.array([16, 0]))
        surface.blit(self.plus, self.hub_grid[1, 2])
        surface.blit(self.font.render("{:2d}".format(int(self.robot.health_regen)), False, (0, 0, 0)),
                     self.hub_grid[1, 2] + np.array([16, 0]))

    def __draw_health_bar(self, surface):
        health = self.robot.health
        max_health = self.robot.max_health
        bar_height = 15

        health_bar_frame = pygame.Rect(self.x-1, self.y - bar_height - 2 - 1, self.width+2, bar_height+2)
        pygame.draw.rect(surface, (0, 0, 0), health_bar_frame)

        health_bar = pygame.Rect(self.x, self.y - bar_height-2, self.width, bar_height)
        pygame.draw.rect(surface, (100, 0, 0), health_bar)

        if health <= max_health:
            r = min(255, 255 - (255 * ((health - (max_health - health)) / max_health)))
            g = min(255, 255 * (health / (max_health / 2)))
            color = (r, g, 0)
            width = int(self.width * health / max_health)
            health_bar = pygame.Rect(self.x, self.y-bar_height-2, width, bar_height)
            pygame.draw.rect(surface, color, health_bar)

            health_text = self.font.render("{:3d} / {:3d}".format(int(health), int(max_health)), False, (0, 0, 0))
            text_rect = health_text.get_rect(center=(self.x + self.width/2, self.y - bar_height / 2 - 2))
            surface.blit(health_text, text_rect)

    def __draw_level(self, surface):
        radius = 18
        center = (self.x + 16 + self.hub_right * 16, self.y + 20)
        pygame.draw.circle(surface, self.frame_color, center, radius+2)
        pygame.draw.circle(surface, self.bg_color, center, radius)
        level_text = self.font.render("{:2d}".format(int(self.robot.level)), False, (0, 0, 0))
        text_rect = level_text.get_rect(center=center)
        surface.blit(level_text, text_rect)

    def __draw_experience_bar(self, surface):
        experience = self.robot.experience
        experience_for_level_up = self.robot.experience_for_level_up
        bar_height = 16
        bar_width = self.width - self.height
        bar_x = self.x + 12*4 + self.hub_right * 16
        bar_y = self.y + 22
        health_bar_frame = pygame.Rect(bar_x-1, bar_y-1, bar_width+2, bar_height+2)
        pygame.draw.rect(surface, (0, 0, 0), health_bar_frame)

        health_bar = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, (0, 100, 100), health_bar)

        if experience <= experience_for_level_up:
            color = (0, 200, 200)
            width = int(bar_width * experience / experience_for_level_up)
            health_bar = pygame.Rect(bar_x, bar_y, width, bar_height)
            pygame.draw.rect(surface, color, health_bar)

            experience_text = self.font.render("{:3d} / {:3d}".format(int(experience), int(experience_for_level_up)),
                                               False, (0, 0, 0))
            text_rect = experience_text.get_rect(center=(bar_x + bar_width/2, bar_y + bar_height / 2 - 2))
            surface.blit(experience_text, text_rect)

    def __draw_buttons(self, surface):
        for button in self.buttons.values():
            button.draw(surface)

    def get_event(self, event, mouse):
        for stat_key, button in self.buttons.items():
            if stat_key == "self_speed" and self.robot.self_speed >= self.robot.max_self_speed:
                button.selectable = False
            elif stat_key == "projectile_initial_speed" and self.robot.projectile_initial_speed >= self.robot.max_projectile_initial_speed:
                button.selectable = False
            else:
                button.selectable = self.robot.experience_points > 0

        x, y = mouse.get_pos()
        mouse_in = self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        if not mouse_in:
            return False
        else:
            for stat_key, button in self.buttons.items():
                clicked = button.get_event(event, mouse)
                if clicked:
                    self.robot.upgrade_stat(stat_key)
            return True

    def draw(self, surface):
        self.__draw_frame(surface)
        self.__draw_buttons(surface)
        self.__draw_stats(surface)
        self.__draw_health_bar(surface)
        self.__draw_level(surface)
        self.__draw_experience_bar(surface)


class Button:
    """
    A class to handle the buttons of the robot hub.
    Source: https://pythonprogramming.altervista.org/buttons-in-pygame/"""

    def __init__(self, pos, shape, selectable, bg=(255, 255, 255), frame=(0, 0, 0)):
        self.x, self.y = pos
        self.width, self.height = shape
        if self.width < 3 or self.height < 3:
            raise ValueError("Button must be at least 3x3.")
        self.selectable = selectable
        self.hover = False
        self.pressed = False

        self.bg = bg
        self.bg_hover = tuple(int(c+(-1)**(c >= 128) * 50) for c in bg)
        self.bg_pressed = tuple(int(c + (-1) ** (c >= 128) * 100) for c in bg)
        self.frame = frame
        self.frame_hover = tuple(int(c+(-1)**(c >= 128) * 50) for c in frame)
        self.frame_pressed = tuple(int(c + (-1) ** (c >= 128) * 100) for c in bg)

    def draw(self, surface):
        button_frame = pygame.Rect(self.x, self.y, self.width, self.height)
        button_inner = pygame.Rect(self.x + 1, self.y + 1, self.width - 2, self.height - 2)
        if self.selectable:
            if self.hover:
                pygame.draw.rect(surface, self.frame_hover, button_frame)
                pygame.draw.rect(surface, self.bg_hover, button_inner)
            elif self.pressed:
                pygame.draw.rect(surface, self.frame_pressed, button_frame)
                pygame.draw.rect(surface, self.bg_pressed, button_inner)
            else:
                pygame.draw.rect(surface, self.frame, button_frame)
                pygame.draw.rect(surface, self.bg, button_inner)
        else:
            pass
            #pygame.draw.rect(surface, self.bg, button_frame)

    def __is_in_button(self, mouse):
        x, y = mouse.get_pos()
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def get_event(self, event, mouse):
        """Returns 1 if clicked."""
        if not self.selectable:
            return 0
        if self.__is_in_button(mouse):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pressed = True
                self.hover = False
                return 0
            elif event.type == pygame.MOUSEBUTTONUP and self.pressed:
                self.pressed = False
                self.hover = True
                return 1
            else:
                self.hover = True
                return 0
        else:
            self.hover = False
            return 0
