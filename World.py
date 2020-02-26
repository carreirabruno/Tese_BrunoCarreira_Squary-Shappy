import pygame
import perceptron
from Wall import *
from game import *
import numpy as np
import time
from Squary import *
import Shappy as sha
from Terrain import *
import random


class World(object):
    pop_names = ["Squary", "Fire", "Shappy", "Wall"]

    def __init__(self, screen_ratio, food_spawn_rate, number_of_scores, update_time, terrain_file, num_directions, shappy_speed, squary_speed, squary_run_distance,
                 learning_rate, epochs, display_on):

        self.shappy_group = pygame.sprite.Group()
        self.squary_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()

        self.shappy_speed = shappy_speed
        self.squary_speed = squary_speed
        self.squary_run_distance = squary_run_distance

        self.display_on = display_on

        self.screen_ratio = screen_ratio
        self.terrain_file = terrain_file
        self.terrain = Terrain(terrain_file)

        self.screen_width = self.terrain.width * self.screen_ratio
        self.screen_height = self.terrain.height * self.screen_ratio

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        self.fov_radius = 100


        # create initial squary
        for squary_boy in self.terrain.initial_squary_list:
            squary = Squary(squary_boy[1] * self.screen_ratio, squary_boy[0] * self.screen_ratio, self.squary_speed, self.squary_speed, self,
                            num_directions, self.squary_run_distance)
            self.squary_group.add(squary)

        # create initial shappy
        for shappy_boy in self.terrain.initial_shappy_list:
            shappy = sha.Shappy(shappy_boy[0], shappy_boy[2] * self.screen_ratio, shappy_boy[1] * self.screen_ratio,
                                self.shappy_speed, self.shappy_speed,
                                self, num_directions, learning_rate, epochs, shappy_boy[3])
            self.shappy_group.add(shappy)

        #create walls
        for line in range(len(self.terrain.matrix)):
            for column in range(len(self.terrain.matrix[0])):
                #print("Line: ", line)
                #print(self.world.terrain.matrix[line])
                #print("Column: ", column)
                #print(self.world.terrain.matrix[line][column])
                if (self.terrain.matrix[line][column] == 1):
                    wall = Wall("Wall", self.screen, column * self.screen_ratio, line * self.screen_ratio, self.screen_ratio, self.screen_ratio)
                    self.wall_group.add(wall)


        self.font = pygame.font.SysFont("Times New Roman", 18)
        self.last_update = None
        self.last_food = time.time()
        self.food_spawn_rate = food_spawn_rate
        self.number_of_scores = number_of_scores
        self.red_blue_score = 0
        self.red_score = 0
        self.blue_score = 0
        self.iteration = 0

        self.update_time = update_time

    def getWidth(self):
        return self.screen_width

    def getHeight(self):
        return self.screen_height

    def spawnNewSquary(self, prev_squary):

        new_x_pos = random.randint(prev_squary.x_size, self.screen_width - prev_squary.x_size)
        new_y_pos = random.randint(prev_squary.y_size, self.screen_height - prev_squary.y_size)

        normalized_new_x_pos = round((new_x_pos*len(self.terrain.matrix))/self.screen_width)
        normalized_new_y_pos = round((new_y_pos*len(self.terrain.matrix[0]))/self.screen_height)

        # Verifica se a nova posiçao está livre
        while self.terrain.matrix[normalized_new_x_pos][normalized_new_y_pos] != 0 \
                and self.terrain.matrix[normalized_new_x_pos][normalized_new_y_pos - 1] != 0 \
                and self.terrain.matrix[normalized_new_x_pos][normalized_new_y_pos + 1] != 0 \
                and self.terrain.matrix[normalized_new_x_pos - 1][normalized_new_y_pos] != 0 \
                and self.terrain.matrix[normalized_new_x_pos - 1][normalized_new_y_pos - 1] != 0 \
                and self.terrain.matrix[normalized_new_x_pos - 1][normalized_new_y_pos + 1] != 0 \
                and self.terrain.matrix[normalized_new_x_pos + 1][normalized_new_y_pos] != 0 \
                and self.terrain.matrix[normalized_new_x_pos + 1][normalized_new_y_pos - 1] != 0 \
                and self.terrain.matrix[normalized_new_x_pos + 1][normalized_new_y_pos + 1] != 0 \
                and self.terrain.matrix[normalized_new_x_pos][normalized_new_y_pos - 2] != 0 \
                and self.terrain.matrix[normalized_new_x_pos][normalized_new_y_pos - 2] != 0 \
                and self.terrain.matrix[normalized_new_x_pos][normalized_new_y_pos + 2] != 0 \
                and self.terrain.matrix[normalized_new_x_pos - 2][normalized_new_y_pos] != 0 \
                and self.terrain.matrix[normalized_new_x_pos - 2][normalized_new_y_pos - 2] != 0 \
                and self.terrain.matrix[normalized_new_x_pos - 2][normalized_new_y_pos + 2] != 0 \
                and self.terrain.matrix[normalized_new_x_pos + 2][normalized_new_y_pos] != 0 \
                and self.terrain.matrix[normalized_new_x_pos + 2][normalized_new_y_pos - 2] != 0 \
                and self.terrain.matrix[normalized_new_x_pos + 2][normalized_new_y_pos + 2] != 0:

            new_x_pos = random.randint(prev_squary.x_size, self.screen_width - prev_squary.x_size)
            new_y_pos = random.randint(prev_squary.y_size, self.screen_height - prev_squary.y_size)

            normalized_new_x_pos = round((new_x_pos * len(self.terrain.matrix)) / self.screen_width)
            normalized_new_y_pos = round((new_y_pos * len(self.terrain.matrix[0])) / self.screen_height)

        squary = Squary(new_x_pos, new_y_pos, self.squary_speed, self.squary_speed, self,
                        prev_squary.num_directions, self.squary_run_distance)
        self.squary_group.add(squary)

    def update(self):

        # first time
        if self.last_update == None:
            self.last_update = time.time()
            return

        delta_t = time.time() - self.last_update

        if delta_t >= self.update_time:
            self.iteration += 1
           # addGameState(self, self.iteration)

            # sprite way
            self.shappy_group.update(delta_t)
            self.squary_group.update(delta_t)

            # for dude in self.shappy_group:
            #     dude.rect.x += dude.x_speed * delta_t
            #     dude.rect.y += dude.y_speed * delta_t

            # self.squary_group.update()
            #
            # for each in self.squary_group:
            #     each.x_pos += each.x_speed * delta_t
            #     each.y_pos += each.y_speed * delta_t

            # print(random.randint(-1, 1))
            # x = each.rect.x
            # y = each.rect.y
            # each.rect.x += random.randint(-5, 5)
            # each.rect.y += random.randint(-5, 5)
            #
            # print (x - each.rect.x)
            # print (y - each.rect.y)
            self.last_update = time.time()

    def render(self):

        # add background over all past images
        self.screen.fill((255, 255, 255))

        # first = True
        # for item in room1_walls:
        #     wall = Wall(item[0], item[1], item[2], item[3], item[4])
        #     if first:
        #         self.screen.blit(self.font.render("1", 1, (0, 0, 0)), (item[1] + 20, item[2] + 20))
        #         first = False
        #     self.wall_group.add(wall)
        #
        # first = True
        # for item in room2_walls:
        #     wall = Wall(item[0], item[1], item[2], item[3], item[4])
        #     if first:
        #         self.screen.blit(self.font.render("2", 1, (0, 0, 0)), (item[1] + 20, item[2] + 20))
        #         first = False
        #     self.wall_group.add(wall)

        # the sprite way
        self.wall_group.draw(self.screen)
        self.shappy_group.draw(self.screen)
        self.squary_group.draw(self.screen)

        #LINE OF SIGHT
        for s in self.shappy_group:
            center_x = int(round(s.rect.x + s.rect.width / 2))
            center_y = int(round(s.rect.y + s.rect.height / 2))

            for sq in self.squary_group:
                sq_center_x = int(round(sq.rect.x + sq.rect.width / 2))
                sq_center_y = int(round(sq.rect.y + sq.rect.height / 2))

                # if (math.sqrt((center_x - sq_center_x)**2 + (center_y - sq_center_y)**2) < 150) \
                #         and self.check_line_of_sight(center_x, center_y, sq_center_x, sq_center_y) is True:
                       # line = pygame.draw.line(self.screen, (0, 255, 0), (center_x, center_y), (sq_center_x, sq_center_y), 3)

            #For FOV2
            # corner1 = (center_x, center_y)
            # corner2 = (center_x, center_y)
            # if s.get_direction()[0] == 0 and s.get_direction()[1] > 0:  #DOWN
            #     corner1 = (center_x - self.fov_radius, center_y + self.fov_radius)
            #     corner2 = (center_x + self.fov_radius, center_y + self.fov_radius)
            # elif s.get_direction()[0] == 0 and s.get_direction()[1] < 0:  #UP
            #     corner1 = (center_x - self.fov_radius, center_y - self.fov_radius)
            #     corner2 = (center_x + self.fov_radius, center_y - self.fov_radius)
            # elif s.get_direction()[0] > 0 and s.get_direction()[1] == 0:  #RIGHT
            #     corner1 = (center_x + self.fov_radius, center_y - self.fov_radius)
            #     corner2 = (center_x + self.fov_radius, center_y + self.fov_radius)
            # elif s.get_direction()[0] < 0 and s.get_direction()[1] == 0:  #LEFT
            #     corner1 = (center_x - self.fov_radius, center_y - self.fov_radius)
            #     corner2 = (center_x - self.fov_radius, center_y + self.fov_radius)
            #  FALTA FAZER PARA OS CANTOS

            #line = pygame.draw.line(self.screen,(0,255,0), (center_x, center_y),((center_x+s.get_direction()[0]*20),(center_y+s.get_direction()[1]*20)), 3)
            # FOV1 = pygame.draw.circle(self.screen, (0,0,0), (center_x, center_y), 150, 1)
            #FOV2 = pygame.draw.polygon(self.screen, (0,255,0), [[center_x, center_y], corner1, corner2], 2)

        if self.number_of_scores == "single":

            self.red_blue_score = 0

            for dude in self.shappy_group:
                self.red_blue_score += dude.score

            score_rend = self.font.render("Red & Blue: " + str(self.red_blue_score), 1, (0, 0, 0))
            self.screen.blit(score_rend, (20, 20))
        elif self.number_of_scores == "double":
            self.red_score = 0
            self.blue_score = 0

            for dude in self.shappy_group:
                if dude.name == "A":
                    self.red_score += dude.score
                if dude.name == "B":
                    self.blue_score += dude.score

            score_red_rend = self.font.render("Red: " + str(self.red_score), 1, (0, 0, 0))
            self.screen.blit(score_red_rend, (20, 20))

            score_blue_rend = self.font.render("Blue: " + str(self.blue_score), 1, (0, 0, 0))
            self.screen.blit(score_blue_rend, (20, 40))

        pygame.display.flip()

    def check_line_of_sight(self, x1, y1, x2, y2):
        pos1_x = int(round((x1 * len(self.terrain.matrix[0]))/self.screen_width))
        pos2_x = int(round((x2 * len(self.terrain.matrix[0]))/self.screen_width))
        pos1_y = int(round((y1 * len(self.terrain.matrix[1]))/self.screen_height))
        pos2_y = int(round((y2 * len(self.terrain.matrix[1]))/self.screen_height))

        big_x = pos1_x
        big_y = pos1_y
        small_x = pos2_x
        small_y = pos2_y

        if pos2_x > pos1_x:
            big_x = pos2_x
            small_x = pos1_x
        if pos2_y > pos1_y:
            big_y = pos2_y
            small_y = pos1_y

        for ind_x in range(small_x, big_x + 1):
            for ind_y in range(small_y, big_y + 1):
                if(self.terrain.matrix[ind_y][ind_x]) == 1:
                    return False

        return True