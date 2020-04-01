import pygame
import os
from oneDBoxes2Scenario.MDP_Centralized_policy_maker_oneDBoxes2 import *
from oneDBoxes2Scenario.MDP_Decentralized_policy_maker_oneDBoxes2 import *
from oneDBoxes2Scenario.World_oneDBoxes2 import *
from oneDBoxes2Scenario.Terrain_oneDBoxes2 import *

def main():

    centralized_policy_map1_file = "oneDBoxes2_MDP_centralized_policy_map1.pickle"
    centralized_policy_map2_file = "oneDBoxes2_MDP_centralized_policy_map2.pickle"

    decentralized_policy_map1_file = "oneDBoxes2_MDP_decentralized_policy_map1.pickle"
    decentralized_policy_map2_file = "oneDBoxes2_MDP_decentralized_policy_map2.pickle"


    terrain1 = Terrain_oneDBoxes2("oneDBoxes2_map1.txt")
    terrain2 = Terrain_oneDBoxes2("oneDBoxes2_map2.txt")


    #create the policy
    # policy_maker_map1 = MDP_Centralized_policy_maker_oneDBoxes2(terrain1.matrix, centralized_policy_map2_file)
    # policy_maker_map2 = MDP_Centralized_policy_maker_oneDBoxes2(terrain2.matrix, centralized_policy_map2_file)

    decentralized_policy_maker1 = MDP_Decentralized_policy_maker_oneDBoxes2(terrain1.matrix, decentralized_policy_map1_file)
    # decentralized_policy_maker2 = MDP_Decentralized_policy_maker_oneDBoxes2(terrain2.matrix, decentralized_policy_map2_file)


    # define a variable to control the main loop
    running = True

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    pygame.display.set_caption("Boxes")

    # game window centered on start
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    #create world
    world = World_oneDBoxes2(terrain1, decentralized_policy_map1_file)

    world.render()

    # main loop
    while running:
        world.update()
        world.render()

        if len(world.box_group) == 0:
            running = False

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
              posx, posy = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    world.show_automatic = not world.show_automatic
                    for shappy in world.shappy_group:
                        shappy.auto = not shappy.auto
                        shappy.calculate = True


if __name__ == "__main__":
    # call the main function
    main()