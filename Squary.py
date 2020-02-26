import pygame
import time
import numpy as np
from World import *
import math
import perceptron
import random


def get_center(sprite):
    return (sprite.rect.x + sprite.rect.width / 2, sprite.rect.y + sprite.rect.height / 2)

class Squary(pygame.sprite.Sprite):
    score_provided = 10
    last_time = 0
    size = 20
    cornered = 0
    run_vec = [0,0]

    def __init__(self, x_pos, y_pos, x_speed, y_speed, world, num_directions, run_distance):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/20-20_green_square.png")
        self.x_size, self.y_size = self.image.get_rect().size
        self.rect = pygame.Rect(x_pos, y_pos, self.x_size, self.y_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.old_x_pos = x_pos
        self.old_y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.run_distance = run_distance
        self.world = world
        self.num_directions = num_directions
        self.last_time = time.time()
        self.angle = random.uniform(0, 2.0 * math.pi)

    def collided(self):

        self.world.spawnNewSquary(self)
        self.kill()

    def update(self, delta_t):

        #print("SQUARYX: ", self.rect.x)
        #print("SQUARYY: ", self.rect.y)

        self.old_x_pos = self.x_pos
        self.old_y_pos = self.y_pos

        self.collision_check()


        # get angle of objects
        #perc_vec = self.get_perception_vec(12)
        ################################## We need to make this scale with len(pop_names)
        #uni = np.concatenate((perc_vec[0], perc_vec[1])).tolist()
        #print(uni)

        #self.x_pos += perc_vec[0] * 10
        #self.y_pos += perc_vec[1] * 10
        #print(deltaTime)

        self.dir_vector = self.get_direction()

        self.x_pos += (self.dir_vector[0]) * delta_t
        self.y_pos -= (self.dir_vector[1]) * delta_t


        # self.x_pos += np.random.uniform(-100, 100)*delta_t
        # self.y_pos += np.random.uniform(-100, 100)*delta_t
        #self.last_time = time.time()

        self.general_collision()


        # collided_walls = self.wall_collision_check()
        #
        # if collided_walls:
        #
        #     #print("XPOSITION: ", self.rect.x)
        #     #print("YPOSITION: ", self.rect.y)
        #     self.rect.x = old_x_pos
        #     self.rect.y = old_y_pos

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

       # self.rect.x += np.random.uniform(, 3)
       # print(self.rect.x)
       # self.rect.y += np.random.uniform(-3, 3)


    def collision_check(self):
        

        for dude in self.world.shappy_group:
             if pygame.sprite.collide_mask(self, dude):
                dude.score += self.score_provided
                self.collided()
                return
    
        # wall check
        # if (self.rect.x + self.rect.width) > self.world.getWidth():
        #     self.rect.x = self.world.getWidth() - self.rect.width
        #     self.x_speed = 0
        # if self.rect.x < 0:
        #     self.rect.x = 0
        #     self.x_speed = 0
        # if (self.rect.y + self.rect.height) > self.world.getHeight():
        #     self.rect.y = self.world.getHeight() - self.rect.height
        #     self.y_speed = 0
        # if self.rect.y < 0:
        #     self.rect.y = 0
        #     self.y_speed = 0

    def get_random_direction(self):

        # angle = random.uniform(0, 2.0 * math.pi)
        # vector = [-self.x_speed * math.cos(angle - math.pi), self.y_speed * math.sin(angle - math.pi)]
        #
        # print("random: ", vector)
        #
        # dividiv = abs(vector[0]) + abs(vector[1])
        #
        # vector[0] /= dividiv
        # vector[1] /= dividiv
        #
        # print("normalized: ", vector)

        rand_inc = random.uniform(-2.0 * math.pi, 2.0 * math.pi)/20

        if(self.angle + rand_inc) > 2.0 * math.pi:
            self.angle = (self.angle + rand_inc) - 2.0 * math.pi
        else:
            self.angle += rand_inc

        vector = [(-self.x_speed * math.cos(self.angle - math.pi))/2, (self.y_speed * math.sin(self.angle - math.pi))/2]

        return vector


    def get_direction(self):

        perc_vec = self.get_perception_vec()
        wall_vector = [0,0]

        indi, = np.where(perc_vec[2] == max(perc_vec[2]))

        if (len(indi) == self.num_directions):
            shappy_vector = self.get_random_direction()

        else:
            # print("indi: ", indi)
            angle = (((2.0 * math.pi) / self.num_directions) * indi[0]) + (((2.0 * math.pi) / self.num_directions) / 2)
            self.angle = angle
            # print("angle: ", angle)
            shappy_vector = [-self.x_speed * math.cos(angle - math.pi), self.y_speed * math.sin(angle - math.pi)]
            # print("vector: ", shappy_vector)

            indi_walls, = np.where(perc_vec[3] == min(perc_vec[3]))

            if (len(indi_walls) != self.num_directions):

                for indi_wally in indi_walls:
                    angle = (((2.0 * math.pi) / self.num_directions) * indi_wally) + (
                                ((2.0 * math.pi) / self.num_directions) / 2)
                    wall_vector[0] += self.x_speed * math.cos(angle - math.pi)
                    wall_vector[1] += -self.y_speed * math.sin(angle - math.pi)




            indi_walls, = np.where(perc_vec[3] == max(perc_vec[3]))

            #print(indi_walls)

            if (len(indi_walls) != self.num_directions):

                for indi_wally in indi_walls:

                    # print("indi: ", indi)
                    angle = (((2.0 * math.pi) / self.num_directions) * indi_wally) + (((2.0 * math.pi) / self.num_directions) / 2)
                    # print("angle: ", angle)
                    if (shappy_vector[1] < 0):
                        if (shappy_vector[0] < 0):
                            wall_vector[1] += (self.x_speed * math.cos(angle - math.pi))
                            wall_vector[0] += -(self.y_speed * math.sin(angle - math.pi))
                        else:
                            wall_vector[1] += -(self.x_speed * math.cos(angle - math.pi))
                            wall_vector[0] += (self.y_speed * math.sin(angle - math.pi))
                        if (shappy_vector[0] < 0):
                            wall_vector[1] += (-self.x_speed * math.cos(angle - math.pi))
                            wall_vector[0] += (self.y_speed * math.sin(angle - math.pi))
                        else:
                            wall_vector[1] += (self.x_speed * math.cos(angle - math.pi))
                            wall_vector[0] += -(self.y_speed * math.sin(angle - math.pi))

                    # if (shappy_vector[0] < 0):
                    #     wall_vector[0] += (self.y_speed * math.sin(angle - math.pi))/len(indi_walls)
                    # else:
                    #     wall_vector[0] += -(self.y_speed * math.sin(angle - math.pi))/len(indi_walls)
                    # print("vector: ", vector)



        #print(wall_vector)
        #print(shappy_vector)

        vector = [0,0]
        vector[0] = wall_vector[0] + shappy_vector[0]*3
        vector[1] = wall_vector[1] + shappy_vector[1]*3

        dividiv = abs(vector[0]) + abs(vector[1])
        if dividiv == 0:
            return [0,0]
        vector[0] /= dividiv
        vector[1] /= dividiv
        vector[0] *= self.x_speed
        vector[1] *= self.y_speed

        #print(vector)
        return vector

    def wall_collision_check(self):

        collided_walls = []

        for wally in self.world.wall_group:
            if pygame.sprite.collide_mask(self, wally):
                collided_walls.append(wally)

        return collided_walls

    def general_collision(self):
        proposed_x_list = []

        proposed_y_list = []

        # Collision for the x axis
        collisions = self.matrix_colision(self.x_pos, self.old_y_pos)

        for collicollix in collisions:

            if (collicollix[0] * self.world.screen_ratio + self.world.screen_ratio) <= self.x_pos + (self.size / 2):
                pass
            elif (collicollix[0] * self.world.screen_ratio) <= (self.x_pos + self.size):

                if (self.x_pos - (collicollix[0] * self.world.screen_ratio - self.size)) <= (
                        self.x_pos - self.old_x_pos):
                    # self.x_pos = collicollix[0] * self.world.screen_ratio - self.size
                    # print("COLLILII: ", collicollix[0])
                    # print("XPOS: ", self.x_pos)
                    # print("Right Collision!")
                    proposed_x_list.append(collicollix[0] * self.world.screen_ratio - self.size)
                    continue

            if (collicollix[0] * self.world.screen_ratio) > (self.x_pos + (self.size / 2)):
                pass
            elif (collicollix[0] * self.world.screen_ratio + self.world.screen_ratio) > self.x_pos:

                if ((collicollix[0] * self.world.screen_ratio + self.world.screen_ratio) - self.x_pos) <= (
                        self.old_x_pos - self.x_pos):
                    # self.x_pos = collicollix[0] * self.world.screen_ratio + self.world.screen_ratio
                    proposed_x_list.append(collicollix[0] * self.world.screen_ratio + self.world.screen_ratio)
                    # print("COLLILII: ", collicollix[0])
                    # print("XPOS: ", self.x_pos)
                    # print("Left Collision!")
                    continue

        # Collision for the y axis
        collisions = self.matrix_colision(self.old_x_pos, self.y_pos)
        for collicolliy in collisions:

            if (collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio) <= (self.y_pos + (self.size / 2)):
                pass
            elif (collicolliy[1] * self.world.screen_ratio) <= (self.y_pos + self.size):

                if abs(self.y_pos - (
                        collicolliy[1] * self.world.screen_ratio - self.size)) <= abs(self.y_pos - self.old_y_pos):
                    # self.y_pos = collicolliy[1] * self.world.screen_ratio - self.size
                    proposed_y_list.append(collicolliy[1] * self.world.screen_ratio - self.size)
                    # print("COLLILII: ", collicolliy[1])
                    # print("YPOS: ", self.y_pos)
                    # print("Down Collision!")
                    continue

            if (collicolliy[1] * self.world.screen_ratio) > (self.y_pos + (self.size / 2)):
                pass
            elif (collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio) > self.y_pos:

                if abs(self.y_pos - (
                        collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio)) <= abs(
                    self.y_pos - self.old_y_pos):
                    # self.y_pos = collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio
                    proposed_y_list.append(collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio)
                    # print("COLLILII: ", collicolliy[1])
                    # print("YPOS: ", self.y_pos)
                    # print("Up Collision!")
                    continue

        min_alt_x = math.inf
        for alt_x in proposed_x_list:
            if abs(self.x_pos - alt_x) < abs(self.x_pos - min_alt_x):
                min_alt_x = alt_x

        min_alt_y = math.inf
        for alt_y in proposed_y_list:
            if abs(self.y_pos - alt_y) < abs(self.y_pos - min_alt_y):
                min_alt_y = alt_y

        if min_alt_x != math.inf:
            self.x_pos = min_alt_x

        if min_alt_y != math.inf:
            self.y_pos = min_alt_y

        # run collision for both x and y to avoid corner bug
        collisions = self.matrix_colision(self.x_pos, self.y_pos)

        for collicollix in collisions:

            if (collicollix[0] * self.world.screen_ratio + self.world.screen_ratio) <= self.x_pos + (self.size / 2):
                pass
            elif (collicollix[0] * self.world.screen_ratio) <= (self.x_pos + self.size):

                if (self.x_pos - (collicollix[0] * self.world.screen_ratio - self.size)) <= (
                        self.x_pos - self.old_x_pos):
                    # self.x_pos = collicollix[0] * self.world.screen_ratio - self.size
                    proposed_x_list.append(collicollix[0] * self.world.screen_ratio - self.size)
                    continue

            if (collicollix[0] * self.world.screen_ratio) > (self.x_pos + (self.size / 2)):
                pass
            elif (collicollix[0] * self.world.screen_ratio + self.world.screen_ratio) > self.x_pos:

                if ((collicollix[0] * self.world.screen_ratio + self.world.screen_ratio) - self.x_pos) <= (
                        self.old_x_pos - self.x_pos):
                    # self.x_pos = collicollix[0] * self.world.screen_ratio + self.world.screen_ratio
                    proposed_x_list.append(collicollix[0] * self.world.screen_ratio + self.world.screen_ratio)
                    continue

        for collicolliy in collisions:

            if (collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio) <= (self.y_pos + (self.size / 2)):
                pass
            elif (collicolliy[1] * self.world.screen_ratio) <= (self.y_pos + self.size):

                if abs(self.y_pos - (
                        collicolliy[1] * self.world.screen_ratio - self.size)) <= abs(self.y_pos - self.old_y_pos):
                    # self.y_pos = collicolliy[1] * self.world.screen_ratio - self.size
                    proposed_y_list.append(collicolliy[1] * self.world.screen_ratio - self.size)
                    continue

            if (collicolliy[1] * self.world.screen_ratio) > (self.y_pos + (self.size / 2)):
                pass
            elif (collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio) > self.y_pos:

                if abs(self.y_pos - (
                        collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio)) <= abs(
                    self.y_pos - self.old_y_pos):
                    # self.y_pos = collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio
                    proposed_y_list.append(collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio)
                    continue

        min_alt_x = math.inf
        for alt_x in proposed_x_list:
            if abs(self.x_pos - alt_x) < abs(self.x_pos - min_alt_x):
                min_alt_x = alt_x

        min_alt_y = math.inf
        for alt_y in proposed_y_list:
            if abs(self.y_pos - alt_y) < abs(self.y_pos - min_alt_y):
                min_alt_y = alt_y

        if min_alt_x != math.inf:
            self.x_pos = min_alt_x

        if min_alt_y != math.inf:
            self.y_pos = min_alt_y

    def matrix_colision(self, x_pos, y_pos):
        # Here we will implement the matrix collision. For that, we need the central position of the shappy.
        # We want to be independent from pygame, so we'll need to create a way to have the central postion wihout the rect thingy thing
        # Having the central position, we can find the overlapping positions in the matrix and access if there was or not a collision

        collision_list = []

        # print("X: ", self.x_pos)
        # print("Y: ", self.y_pos)
        # print("Floored X: ", int(math.floor(self.x_pos / self.world.screen_ratio)))
        # print("Ceiled X + 30: ", int(math.ceil((self.x_pos + self.size) / self.world.screen_ratio)))

        floored_x = int(math.floor(x_pos / self.world.screen_ratio))
        ceiled_x = int(math.ceil((x_pos + self.size) / self.world.screen_ratio))

        # print("Floored y: ", int(math.floor(self.y_pos / self.world.screen_ratio)))
        # print("Ceiled Y + 30: ", int(math.ceil((self.y_pos + self.size) / self.world.screen_ratio)))

        floored_y = int(math.floor(y_pos / self.world.screen_ratio))
        ceiled_y = int(math.ceil((y_pos + self.size) / self.world.screen_ratio))

        if floored_x < 0:
            floored_x = 0

        if floored_y < 0:
            floored_y = 0

        if ceiled_x > len(self.world.terrain.matrix[0]):
            ceiled_x = len(self.world.terrain.matrix[0])

        if ceiled_y > len(self.world.terrain.matrix):
            ceiled_y = len(self.world.terrain.matrix)

        for xxx in range(floored_x, ceiled_x):
            for yyy in range(floored_y, ceiled_y):

                if self.world.terrain.matrix[yyy][xxx] == 1:
                    collision_list.append([xxx, yyy])
        return collision_list

    def get_perception_vec(self):

        myX, myY = get_center(self)

        dist_q_array = np.full((len(self.world.pop_names), self.num_directions), 0)

        for poppy in self.world.shappy_group:
            targetX, targetY = get_center(poppy)

            myradians = math.atan2(targetY - myY, targetX - myX)
            # print("My radians: ", myradians)
            pos_radians = myradians + math.pi
            quadrant = int(pos_radians // ((2 * math.pi) / self.num_directions))
            if quadrant == self.num_directions:
                quadrant -= 1
            distance = math.hypot(targetX - myX, targetY - myY)
            # print(distance)

            if distance > self.run_distance:
                dist_q_array[self.world.pop_names.index(type(poppy).__name__)][quadrant] = 0
            else:
                dist_q_array[self.world.pop_names.index(type(poppy).__name__)][quadrant] = abs(
                    math.sqrt(self.world.screen_width ** 2 + self.world.screen_height ** 2) - distance)
                # print(dist_q_array)
                # print(type(poppy).__name__)


        for wally in self.world.wall_group:
            targetX, targetY = get_center(wally)

            myradians = math.atan2(targetY - myY, targetX - myX)
            # print("My radians: ", myradians)
            pos_radians = myradians + math.pi
            quadrant = int(pos_radians // ((2 * math.pi) / self.num_directions))
            if quadrant == self.num_directions:
                quadrant -= 1
            distance = math.hypot(targetX - myX, targetY - myY)
            # print(distance)

            if distance > 40:
                dist_q_array[self.world.pop_names.index(type(wally).__name__)][quadrant] = 0
            else:
                dist_q_array[self.world.pop_names.index(type(wally).__name__)][quadrant] = abs(
                    math.sqrt(self.world.screen_width ** 2 + self.world.screen_height ** 2) - distance)
                # print(dist_q_array)
                # print(type(poppy).__name__)


        #print(dist_q_array)
        return dist_q_array
