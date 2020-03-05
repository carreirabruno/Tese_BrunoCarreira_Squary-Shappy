import pygame
import os
from twoDBoxesScenario.Collaborator_twoDBoxes import *
from twoDBoxesScenario.World_twoDBoxes import *


def main():
    # define a variable to control the main loop
    running = True

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    pygame.display.set_caption("Boxes")

    # game window centered on start
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    update_time = 0.1

    #create world
    world = World_twoDBoxes("twoDBoxes_map1.txt")
    #create the collaboration analyser
    #collaborator = Collaborator_twoDBoxes(world, False)
    world.render()

    #createNewLogFile(world)

    # world.show_automatic = not world.show_automatic
    # for shappy in world.shappy_group:
    #     # if shappy.type == "Coolaborative":
    #     shappy.auto = not shappy.auto
    #     shappy.calculate = True

    # main loop
    while running:
        world.update()
        world.render()

        #collaborator.update()

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                #collaborator.write_in_txt()
                running = False
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONDOWN:
              posx, posy = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    world.show_automatic = not world.show_automatic
                    for shappy in world.shappy_group:
                        # if shappy.type == "Collaborative":
                        shappy.auto = not shappy.auto
                        shappy.calculate = True
        if len(world.box_group) == 0:
            running = False

if __name__ == "__main__":
    # call the main function
    main()