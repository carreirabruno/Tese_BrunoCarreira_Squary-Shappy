import pygame
import os
from oneDBoxesScenario.Collaborator_oneDBoxes import *
from oneDBoxesScenario.MDP_Collaborator_oneDBoxes import *
from oneDBoxesScenario.World_oneDBoxes import *
from oneDBoxesScenario.Terrain_oneDBoxes import *
import winsound

def main():
    base_policy_file = "oneDBoxes_MDP_base_policy.txt"
    collaborative_policy_file = "oneDBoxes_MDP_collaborative_policy.txt"
    non_collaborative_policy_file = "oneDBoxes_MDP_non_collaborative_policy.txt"

    terrain = Terrain_oneDBoxes("oneDBoxes_map2.txt")

    #create the policy
    #collaborator = MDP_Collaborator_oneDBoxes(terrain.matrix, non_collaborative_policy_file)
    #winsound.Beep(600, 500)
    #winsound.Beep(600, 1000)

    # define a variable to control the main loop
    running = True

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    pygame.display.set_caption("Boxes")

    # game window centered on start
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    #create world
    world = World_oneDBoxes(terrain, non_collaborative_policy_file)

    #create the collaboration analyser
    #collaborator = Collaborator_oneDBoxes(world, False)

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

    #    collaborator.update()

        if len(world.box_group) == 0:
            running = False

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
         #       collaborator.write_in_txt()
                running = False
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONDOWN:
              posx, posy = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    world.show_automatic = not world.show_automatic
                    for shappy in world.shappy_group:
                       # if shappy.type == "Coolaborative":
                        shappy.auto = not shappy.auto
                        shappy.calculate = True
                if event.key == pygame.K_2:
                    for shappy in world.shappy_group:
                        shappy.go_ahead = True

if __name__ == "__main__":
    # call the main function
    main()
