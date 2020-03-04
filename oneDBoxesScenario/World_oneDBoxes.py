import pygame
from oneDBoxesScenario.Terrain_oneDBoxes import *
from oneDBoxesScenario.oneDBox import *
from oneDBoxesScenario.Shappy_oneDBoxes import *

class World_oneDBoxes(object):

    def __init__(self, terrain_file):

        self.last_update = None

        self.screen_ratio = 10

        self.terrain_file = terrain_file

        self.terrain = Terrain_oneDBoxes(terrain_file)

        self.screen_width = len(self.terrain.matrix[0]) * self.screen_ratio
        self.screen_height = len(self.terrain.matrix) * self.screen_ratio

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        self.fov_radius = 100

        self.font = pygame.font.SysFont("Times New Roman", 18)

        self.score = 0

        self.shappy_speed = 100     #não faz nada, eles mexem-se sempre 1 casa

        self.shappy_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()

        self.show_automatic = False

        #create walls
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 1:
                    wall = Wall("Wall", self.screen, column * self.screen_ratio, line * self.screen_ratio,
                                self.screen_ratio, self.screen_ratio)
                    self.wall_group.add(wall)

        # #create boxes
        # for box_var in self.terrain.initial_boxes_list:
        #     box = Box(box_var[0] * self.screen_ratio, box_var[1] * self.screen_ratio, self)
        #     self.box_group.add(box)

        # #create boxes
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 2:
                    box = oneDBox(column * self.screen_ratio, line * self.screen_ratio)
                    self.box_group.add(box)

        #create shappys
        for shappy_var in self.terrain.initial_shappy_list:

            shappy = Shappy_oneDBoxes(shappy_var[0],shappy_var[1], shappy_var[3] * self.screen_ratio, shappy_var[2] * self.screen_ratio,
                                self.shappy_speed, self.shappy_speed, self, shappy_var[4],
                                self.terrain.matrix, self.screen_width, self.screen_height, False)
            self.shappy_group.add(shappy)

    def render(self):
        # add background over all past images
        self.screen.fill((255, 255, 255))

        score_rend = self.font.render("Score: " + str(self.score), 1, (0, 0, 0))
        self.screen.blit(score_rend, (20, 20))

        self.shappy_group.draw(self.screen)
        self.box_group.draw(self.screen)
        self.wall_group.draw(self.screen)

        if self.show_automatic:
            automatic_rend = self.font.render("Automatic", 1, (255, 0, 0))
            self.screen.blit(automatic_rend, (20, 40))

        pygame.display.flip()

    def check_collisions(self):

        for shappy in self.shappy_group:
            normalized_x_pos = round((shappy.x_pos * len(self.terrain.matrix[0])) / self.screen_width)
            normalized_y_pos = round((shappy.y_pos * len(self.terrain.matrix)) / self.screen_height)

            if self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos] == 2:
                self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos] = 0
                self.box_group_remove(normalized_x_pos * self.screen_ratio,
                                      (normalized_y_pos + 1) * self.screen_ratio)
                self.score += 1
            # elif self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos + 1] == 2:
            #     self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos + 1] = 0
            #     self.box_group_remove((normalized_x_pos + 1) * self.screen_ratio,
            #                           (normalized_y_pos + 1) * self.screen_ratio)
            #     self.score += 1
            # elif self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos - 1] == 2:
            #     self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos - 1] = 0
            #     self.box_group_remove((normalized_x_pos - 1) * self.screen_ratio,
            #                           (normalized_y_pos + 1) * self.screen_ratio)
            #     self.score += 1

    def box_group_remove(self, x_pos, y_pos):
        for box in self.box_group:
            if box.x_pos == x_pos and box.y_pos == y_pos:
                self.box_group.remove(box)

    def update(self):
        if self.last_update is None:
            self.last_update = time.time()
            return

        delta_t = time.time() - self.last_update

        self.shappy_group.update(delta_t)

        self.check_collisions()

        self.last_update = time.time()