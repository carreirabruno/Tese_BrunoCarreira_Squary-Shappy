import pygame
import os
from twoDBoxes2Scenario.MDP_Centralized_policy_maker_twoDBoxes2 import *
from twoDBoxes2Scenario.MDP_Decentralized_policy_maker_twoDBoxes2 import *
from twoDBoxes2Scenario.World_twoDBoxes2 import *
from twoDBoxes2Scenario.Terrain_twoDBoxes2 import *
import winsound

def main():

    centralized_policy_file = "twoDBoxes2_MDP_centralized_policy_map1.pickle"
    decentralized_policy_file = "twoDBoxes2_MDP_decentralized_policy_map1.pickle"

    terrain = Terrain_twoDBoxes2("twoDBoxes2_map1.txt")

    #create the policy
    #centralized_policy_maker = MDP_Centralized_policy_maker_twoDBoxes2(terrain.matrix, centralized_policy_file)
    #decentralized_policy_maker = MDP_Decentralized_policy_maker_twoDBoxes2(terrain.matrix, decentralized_policy_file)
    #quit()

    # define a variable to control the main loop
    running = True

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    pygame.display.set_caption("Boxes")

    # game window centered on start
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    #create world
    world = World_twoDBoxes2(terrain, centralized_policy_file)

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
                if event.key == pygame.K_1:
                    world.show_automatic = not world.show_automatic
                    for shappy in world.shappy_group:
                        shappy.auto = not shappy.auto
                        shappy.calculate = True
                if event.key == pygame.K_2:
                    for shappy in world.shappy_group:
                        shappy.go_ahead = True

if __name__ == "__main__":
    # call the main function
    main()
