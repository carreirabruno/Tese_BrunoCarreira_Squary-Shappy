import pygame
import perceptron
from World import *
import numpy as np
import time
import math


def get_center(sprite):
    return sprite.rect.x + sprite.rect.width / 2, sprite.rect.y + sprite.rect.height / 2


class Shappy(pygame.sprite.Sprite):
    auto = -1
    size = 30

    def __init__(self, name, x_pos, y_pos, x_speed, y_speed, world, num_directions, learning_rate, epochs, color):

        pygame.sprite.Sprite.__init__(self)

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.old_x_pos = x_pos
        self.old_y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.score = 0
        self.world = world
        self.num_directions = num_directions
        self.percy = perceptron.Perceptron((num_directions * len(self.world.pop_names)), num_directions, learning_rate,
                                           epochs)
        self.color = color

        self.dir_vector = []

        if self.color == 0:
            self.image = pygame.image.load("Images/30_30_Red_Square.png")
        elif self.color == 1:
            self.image = pygame.image.load("Images/30_30_Blue_Square.png")
        else:
            print("Unknown colour number: ", self.color)

        x_size, y_size = self.image.get_rect().size
        self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = name
        self.dir = (x_pos, y_pos)

    def update(self, delta_t):
        # self.wall_check()

        if self.auto == -1:

            perc_vec = self.get_perception_vec()
            # print("Perc_VEC: ", perc_vec)

            indi, = np.where(perc_vec[0] == max(perc_vec[0]))

            # print("indi: ", indi)

            angle = (((2.0 * math.pi) / self.num_directions) * indi[0]) + (((2.0 * math.pi) / self.num_directions) / 2)

            # print("angle: ", angle)

            vector = [self.x_speed * math.cos(angle - math.pi), self.y_speed * math.sin(angle - math.pi)]

            # print("vector: ", vector)

            keys = pygame.key.get_pressed()
            if self.color == 0:
                if keys[pygame.K_LEFT]:
                    self.x_pos -= self.x_speed * delta_t
                if keys[pygame.K_RIGHT]:
                    self.x_pos += self.x_speed * delta_t
                if keys[pygame.K_UP]:
                    self.y_pos -= self.y_speed * delta_t
                if keys[pygame.K_DOWN]:
                    self.y_pos += self.y_speed * delta_t
            elif self.color == 1:
                if keys[pygame.K_a]:
                    self.x_pos -= self.x_speed * delta_t
                if keys[pygame.K_d]:
                    self.x_pos += self.x_speed * delta_t
                if keys[pygame.K_w]:
                    self.y_pos -= self.y_speed * delta_t
                if keys[pygame.K_s]:
                    self.y_pos += self.y_speed * delta_t

        if self.auto == 1:
            ################Bruno#################
            self.dir_vector = self.get_closest_squary_direction()
            self.x_pos -= (self.dir_vector[0]) * delta_t
            self.y_pos += (self.dir_vector[1]) * delta_t
            ################PEDRO#################
            # # get angle of objectes
            # perc_vec = self.get_perception_vec(12)
            #
            # ################################## We need to make this scale with len(pop_names)
            # uni = np.concatenate((perc_vec[0], perc_vec[1])).tolist()
            #
            # print("----> Vision of ", self.name, ":")
            # print(uni)
            # print("TEST1")
            # print(self.percy.test([uni]))
            # print("TEST2")
            #
            # self.x_speed += np.random.uniform(-50, 50)
            # self.y_speed += np.random.uniform(-50, 50)
            # self.rect.x += self.x_speed * delta_t
            # self.rect.y += self.y_speed * delta_t


        #check collisions
        self.general_collision()


        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

        self.dir = (self.x_pos - self.old_x_pos, self.y_pos - self.old_y_pos)
       # pygame.draw.circle(self.world, (0,0,0), (self.rect.x, self.rect.y), 200)

        self.old_x_pos = self.x_pos
        self.old_y_pos = self.y_pos


    # def wall_check(self):
    #     for wall in self.world.wall_group:
    #         if self.rect.colliderect(wall.rect):
    #             if self.rect.top - wall.rect.bottom == -2:
    #                 self.y_speed = 0
    #                 self.rect.top = wall.rect.bottom
    #             elif self.rect.bottom - wall.rect.top == 2:
    #                 self.y_speed = 0
    #                 self.rect.bottom = wall.rect.top
    #             if self.rect.left - wall.rect.right == -2:
    #                 self.x_speed = 0
    #                 self.rect.left = wall.rect.right
    #             elif self.rect.right - wall.rect.left == 2:
    #                 self.x_speed = 0
    #                 self.rect.right = wall.rect.left
    #         else:
    #             self.y_speed = 100
    #             self.x_speed = 100

    def get_random_direction(self):

        angle = random.uniform(0, 2.0 * math.pi)
        vector = [-self.x_speed * math.cos(angle - math.pi), self.y_speed * math.sin(angle - math.pi)]

        return vector

    def get_direction(self):
        return self.dir

    def get_closest_squary_direction(self):

        perc_vec = self.get_perception_vec()
        # print("Perc_VEC: ", perc_vec)

        indi, = np.where(perc_vec[0] == max(perc_vec[0]))

        if (len(indi) == self.num_directions):
            vector = self.get_random_direction()

        else:
            # print("indi: ", indi)
            angle = (((2.0 * math.pi) / self.num_directions) * indi[0]) + (((2.0 * math.pi) / self.num_directions) / 2)
            # print("angle: ", angle)
            vector = [-self.x_speed * math.cos(angle - math.pi), self.y_speed * math.sin(angle - math.pi)]
            # print("vector: ", vector)

        return vector

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
                        collicolliy[1] * self.world.screen_ratio + self.world.screen_ratio)) <= abs(self.y_pos - self.old_y_pos):
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

    def wall_collision_check(self):

        collided_walls = []

        for wally in self.world.wall_group:
            if pygame.sprite.collide_mask(self, wally):
                collided_walls.append(wally)

        return collided_walls

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

    def get_perception_vec(self):

        myX, myY = get_center(self)

        dist_q_array = np.full((len(self.world.pop_names), self.num_directions), 0)

        for poppy in self.world.squary_group:
            targetX, targetY = get_center(poppy)

            myradians = math.atan2(targetY - myY, targetX - myX)
            # print("My radians: ", myradians)
            pos_radians = myradians + math.pi
            quadrant = int(pos_radians // ((2 * math.pi) / self.num_directions))
            if quadrant == self.num_directions:
                quadrant -= 1
            distance = math.hypot(targetX - myX, targetY - myY)
            # print(distance)
            dist_q_array[self.world.pop_names.index(type(poppy).__name__)][quadrant] = abs(
                math.sqrt(self.world.screen_width ** 2 + self.world.screen_height ** 2) - distance)
            # print(dist_q_array)
            # print(type(poppy).__name__)

        return dist_q_array
