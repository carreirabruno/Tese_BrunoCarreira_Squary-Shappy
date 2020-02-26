# import the pygame module, so you can use it
import pygame
import time
import numpy as np
import math
import perceptron
from Shappy import *
from World import *
from Squary import *
from Fire import *
import os
from LogMaker import *



# define a main function
def main():


    # define a variable to control the main loop
    running = True

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    logo = pygame.image.load("Images/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Shappy")

    # game window centered on start
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    update_time = 0.1


    #create world
    world = World(700, 700, 5, "single", update_time)



    # Outside walls
    outside_walls = [["wall_up", world.screen, 0, 0, world.screen_width, 10],
                     ["wall_down", world.screen, 0, world.screen_height-10, world.screen_width, 10],
                     ["wall_left", world.screen, 0, 0, 10, world.screen_height],
                     ["wall_right", world.screen, world.screen_width-10, 0, 10, world.screen_height]]

    # room1_walls = [[self.screen, self.screen_width-500, 0, 10, 200],
    #                  [self.screen, self.screen_width-500, 300, 500, 10]]
    #
    # room2_walls = [[self.screen, self.screen_width - 500, 400, 10, 200],
    #                [self.screen, self.screen_width - 500, 400, 500, 10]]

    for item in outside_walls:
        wall = Wall(item[0], item[1], item[2], item[3], item[4], item[5])
        world.wall_group.add(wall)




    #create shappy
    shappy = Shappy("Red", 200, 100, 50, 50, world, 12, 0.3, 100, 0)
    world.shappy_group.add(shappy)

    shappy2 = Shappy("Blue", 100, 200, 50, 50, world, 12, 0.3, 100, 1)
    world.shappy_group.add(shappy2)

    squary = Squary(world.screen_width-300, 200, 0, 0, world, 12)
    world.squary_group.add(squary)

    world.render()

    createNewLogFile(world)
    # main loop
    while running:
        world.update()

        world.render()


        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONDOWN:
              posx, posy = pygame.mouse.get_pos()

              # get a list of all sprites that are under the mouse cursor
              #clicked_buttons = [s for s in world.buttons if s.rect.collidepoint(pos)]

             # new_fire = Fire(posx - 10, posy - 10)
              #world.pop_group.add(new_fire)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    shappy.auto = -shappy.auto
                if event.key == pygame.K_2:
                    shappy2.auto = -shappy2.auto


             
             
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()







