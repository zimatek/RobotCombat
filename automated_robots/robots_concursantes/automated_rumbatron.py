import pygame
from automated_robot import AutomatedRobot
from numpy import random
import numpy as np
import sys
# import scipy
# from scipy.spatial.distance import pdist
# from scipy.spatial.distance import squareform
import math



class Rumbatron(AutomatedRobot):
    
    def move_random(self):
        # Randomly decide where to move
        up_down_none = random.randint(3)
        key = random.randint(4)
        # self.set_velocity(vx=-10, vy=10)
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
        return 0

    def decide(self,  other_robot_properties, coins, projectiles):
        """"Returns a projectile object or None."""
        
        self.upgrade_stat(self.stat_keys[6])
        # Randomly decide what to upgrade
        ii = random.randint(len(self.stat_keys), size=3)
        for i in ii:
            self.upgrade_stat(self.stat_keys[i])
            
        # where to move
        myPosition = self.pos
        maximumVelocity = self.self_speed
        # print(maximumVelocity)
        
        coins_number = len(coins.sprites())
        coins_positions_matrix = []
        
        #if coins number is not zero
        if len(coins.sprites()) > 0:
            # coins_positions_matrix = [x.pos for x in coins.sprites()]
            for i in range(coins_number):
                coin_position = coins.sprites()[i].pos
                coins_positions_matrix.append(coin_position)
            
            # coins_positions_matrix.append(myPosition)
            coins_positions_matrix = np.array(coins_positions_matrix)
            matrix_distance = coins_positions_matrix - myPosition
            thetas = np.arctan(matrix_distance[:,1]/matrix_distance[:,0])
            distance_vector = np.linalg.norm(matrix_distance, axis = 1)
            
            Vx = []
            Vy = []
            real_V = []
            thetas2 = thetas.copy()
            for angle in thetas2:
                if angle <= np.pi/4 and angle >= -np.pi/4:
                     Vx.append(maximumVelocity)
                     Vy.append(abs(maximumVelocity*math.tan(angle)))
                     real_V.append(np.sqrt((maximumVelocity**2 + (maximumVelocity**2)*angle**2)))
                else:
                     Vx.append(abs(maximumVelocity/math.tan(angle)))
                     Vy.append(maximumVelocity)
                     real_V.append(np.sqrt((maximumVelocity**2 + (maximumVelocity**2)/angle**2)) )
            
            time_matrix = distance_vector/np.array(real_V)
            index_minimum_time = np.argmin(time_matrix)
            signo = np.sign(matrix_distance)
            # print("---")
            # print(Vx[index_minimum_time])
            # print(Vy[index_minimum_time])
            # print(signo[index_minimum_time,0], signo[index_minimum_time,1])
            
            
            self.set_velocity(vx=signo[index_minimum_time,0]*Vx[index_minimum_time], vy=-signo[index_minimum_time,1]*Vy[index_minimum_time])
                         
            # matrix_distance = myPosition - coins_positions_matrix
            # distance_vector = np.linalg.norm(matrix_distance, axis = 1)
            
            # index_minimum_distance = np.argmin(distance_vector)
            # position_to_move = matrix_distance[index_minimum_distance]

            # # real_velocity = np.sqrt((maximumVelocity**2 + (maximumVelocity**2)/thetas))      
            # # time_matrix = distance_vector/real_velocity
            
            # if coins_number == 8:
            #     # print(real_velocity)
            #     # print("---")
            #     print(thetas)
            #     print(myPosition)
            #     print("----------------")
            #     print(matrix_distance)
            #     print("----------------")
            #     print(coins_positions_matrix)
            #     print("-----------------")
            #     print(distance_vector)
            #     print("-------------------")
            #     print(position_to_move)
            #     sys.exit()
        else:
            self.move_random()                        
        
        

        # if up_down_none == 0:
        #     if key == 0:
        #         self.set_velocity(vy=10)
        #     if key == 1:
        #         self.set_velocity(vy=-10)
        #     if key == 2:
        #         self.set_velocity(vx=10)
        #     if key == 3:
        #         self.set_velocity(vx=-10)
        # elif up_down_none == 1:
        #     if key == 0:
        #         self.stop('up')
        #     if key == 1:
        #         self.stop('down')
        #     if key == 2:
        #         self.stop('right')
        #     if key == 3:
        #         self.stop('left')

        # Decide to cast a basic attack
        position = other_robot_properties["pos"]
        velocity = other_robot_properties["velocity"]
        
        
        return self.cast_basic_attack(np.array([+20+position[0]+10*velocity[0], position[1]+10*velocity[1]]))
        # cast = random.randint(2)
        # if cast == 0:
        #     pos = random.random(2) * np.array([1000, 10000])
        #     if pos[0] < self.rect.x - 100 or pos[0] > self.rect.x + self.rect.width + 100:
        #         if pos[1] < self.rect.y - 100 or pos[1] > self.rect.y + self.rect.height + 100:
        #             return self.cast_basic_attack(pos)
        # else:
        #     return None
