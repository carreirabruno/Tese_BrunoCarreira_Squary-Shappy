# import the pygame module, so you can use it
import pygame
import time
import numpy as np
import math
import perceptron
from World import *
from Shappy import *
from Terrain import *
from Squary import *
from Displayer import *
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


    num_directions = 12
    learning_rate = None
    epochs = None


    update_time = 0.05

    terrain_file = "Maps/map_collaborative.txt"

    screen_ratio = 10

    food_spawn_rate = 5

    display_on = 1

    shappy_speed = 60

    squary_speed = 120

    squary_run_distance = 200

    #create world
    if terrain_file == "Maps/map_collaborative.txt":
        world = World(screen_ratio, food_spawn_rate, "single", update_time, terrain_file, num_directions,  shappy_speed,
                      squary_speed, squary_run_distance, learning_rate, epochs, display_on)
    elif terrain_file == "Maps/map_non_collaborative.txt":
        world = World(screen_ratio, food_spawn_rate, "double", update_time, terrain_file, num_directions, shappy_speed,
                      squary_speed, squary_run_distance, learning_rate, epochs, display_on)
    elif terrain_file == "Maps/map_medium_collaborative.txt":
        world = World(screen_ratio, food_spawn_rate, "double", update_time, terrain_file, num_directions, shappy_speed,
                      squary_speed, squary_run_distance, learning_rate, epochs, display_on)

    for s in world.shappy_group:
        if s.name == "A":
            shappyA = s
        elif s.name == "B":
            shappyB = s

    #dispy_boy = Displayer(world)


    world.render()

    #createNewLogFile(world)
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
                    shappyA.auto = -shappyA.auto
                if event.key == pygame.K_2:
                    shappyB.auto = -shappyB.auto


             
             

if __name__=="__main__":
    # call the main function
    main()







