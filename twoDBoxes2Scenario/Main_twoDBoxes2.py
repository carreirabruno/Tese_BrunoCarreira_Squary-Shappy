import pygame
import os
from twoDBoxes2Scenario.MDP_Centralized_policy_maker_twoDBoxes2 import *
from twoDBoxes2Scenario.MDP_Individual_Decentralized_policy_maker_twoDBoxes2 import *
from twoDBoxes2Scenario.MDP_Peer_Aware_Decentralized_policy_maker_twoDBoxes2 import *
from twoDBoxes2Scenario.World_twoDBoxes2 import *
from twoDBoxes2Scenario.Terrain_twoDBoxes2 import *
import winsound


def main():

    centralized_policy_map1_file = "twoDBoxes2_MDP_centralized_policy_map1.pickle"
    individual_decentralized_split_rewards_policy_map1_file = "twoDBoxes2_MDP_individual_decentralized_split_rewards_policy_map1.pickle"
    peer_aware_decentralized_split_rewards_policy_map1_file = "twoDBoxes2_MDP_peer_aware_decentralized_split_rewards_policy_map1.pickle"

    terrain1 = Terrain_twoDBoxes2("twoDBoxes2_map1.txt")

    # create the policy
    centralized_policy_maker_map1 = MDP_Centralized_policy_maker_twoDBoxes2(terrain1.matrix, centralized_policy_map1_file, True)
    # individual_decentralized_policy_maker_map1 = MDP_Individual_Decentralized_policy_maker_twoDBoxes2(terrain1.matrix, individual_decentralized_split_rewards_policy_map1_file, False)
    # peer_aware_decentralized_policy_maker_map1 = MDP_Peer_Aware_Decentralized_policy_maker_twoDBoxes2(terrain1.matrix, peer_aware_decentralized_split_rewards_policy_map1_file, False)

    quit()

    # define a variable to control the main loop
    running = True

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    pygame.display.set_caption("Boxes")

    # game window centered on start
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    # create world
    world = World_twoDBoxes2(terrain1, centralized_policy_map1_file)
    # world = World_twoDBoxes2(terrain1, individual_decentralized_split_rewards_policy_map1_file)

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
