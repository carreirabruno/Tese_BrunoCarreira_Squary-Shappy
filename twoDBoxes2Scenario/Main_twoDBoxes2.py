import pygame
import os
from twoDBoxes2Scenario.MDP_Centralized_policy_maker_twoDBoxes2 import *
from twoDBoxes2Scenario.MDP_Individual_Decentralized_policy_maker_twoDBoxes2 import *
from twoDBoxes2Scenario.MDP_Peer_Aware_Decentralized_policy_maker_twoDBoxes2 import *
from twoDBoxes2Scenario.MDP_Peer_Listen_Decentralized_policy_maker_twoDBoxes2 import *
from twoDBoxes2Scenario.Analyser_twoDBoxes2 import *
from twoDBoxes2Scenario.World_twoDBoxes2 import *
from twoDBoxes2Scenario.Terrain_twoDBoxes2 import *
import winsound


def main():

    centralized_policy_map1_file = "twoDBoxes2_MDP_centralized_policy_map1.pickle"
    individual_decentralized_split_rewards_policy_map1_file = "twoDBoxes2_MDP_individual_decentralized_split_rewards_policy_map1.pickle"
    peer_aware_decentralized_split_rewards_policy_map1_file = "twoDBoxes2_MDP_peer_aware_decentralized_split_rewards_policy_map1.pickle"
    peer_listen_decentralized_split_rewards_policy_map1_file = "twoDBoxes2_MDP_peer_listen_decentralized_split_rewards_policy_map1.pickle"

    centralized_policy_map2_file = "twoDBoxes2_MDP_centralized_policy_map2.pickle"
    individual_decentralized_split_rewards_policy_map2_file = "twoDBoxes2_MDP_individual_decentralized_split_rewards_policy_map2.pickle"
    peer_aware_decentralized_split_rewards_policy_map2_file = "twoDBoxes2_MDP_peer_aware_decentralized_split_rewards_policy_map2.pickle"
    peer_listen_decentralized_split_rewards_policy_map2_file = "twoDBoxes2_MDP_peer_listen_decentralized_split_rewards_policy_map2.pickle"
    
    centralized_policy_map3_file = "twoDBoxes2_MDP_centralized_policy_map3.pickle"
    individual_decentralized_split_rewards_policy_map3_file = "twoDBoxes2_MDP_individual_decentralized_split_rewards_policy_map3.pickle"
    peer_aware_decentralized_split_rewards_policy_map3_file = "twoDBoxes2_MDP_peer_aware_decentralized_split_rewards_policy_map3.pickle"
    peer_listen_decentralized_split_rewards_policy_map3_file = "twoDBoxes2_MDP_peer_listen_decentralized_split_rewards_policy_map3.pickle"


    terrain1 = Terrain_twoDBoxes2("twoDBoxes2_map1.txt")
    terrain2 = Terrain_twoDBoxes2("twoDBoxes2_map2.txt")
    terrain3 = Terrain_twoDBoxes2("twoDBoxes2_map3.txt")

    # create the policy
    # centralized_policy_maker_map1 = MDP_Centralized_policy_maker_twoDBoxes2(terrain1.matrix, centralized_policy_map1_file, True)
    # individual_decentralized_policy_maker_map1 = MDP_Individual_Decentralized_policy_maker_twoDBoxes2(terrain1.matrix, individual_decentralized_split_rewards_policy_map1_file, False)
    # peer_aware_decentralized_policy_maker_map1 = MDP_Peer_Aware_Decentralized_policy_maker_twoDBoxes2(terrain1.matrix, peer_aware_decentralized_split_rewards_policy_map1_file, False)
    # peer_listen_decentralized_policy_maker_map1 = MDP_Peer_Listen_Decentralized_policy_maker_twoDBoxes2(terrain1.matrix, peer_listen_decentralized_split_rewards_policy_map1_file, False)

    # centralized_policy_maker_map2 = MDP_Centralized_policy_maker_twoDBoxes2(terrain2.matrix, centralized_policy_map2_file, True)
    # individual_decentralized_policy_maker_map2 = MDP_Individual_Decentralized_policy_maker_twoDBoxes2(terrain2.matrix, individual_decentralized_split_rewards_policy_map2_file, False)
    # peer_aware_decentralized_policy_maker_map2 = MDP_Peer_Aware_Decentralized_policy_maker_twoDBoxes2(terrain2.matrix, peer_aware_decentralized_split_rewards_policy_map2_file, False)
    # peer_listen_decentralized_policy_maker_map2 = MDP_Peer_Listen_Decentralized_policy_maker_twoDBoxes2(terrain2.matrix, peer_listen_decentralized_split_rewards_policy_map2_file, False)

    # centralized_policy_maker_map3 = MDP_Centralized_policy_maker_twoDBoxes2(terrain3.matrix, centralized_policy_map3_file, True)
    # individual_decentralized_policy_maker_map3 = MDP_Individual_Decentralized_policy_maker_twoDBoxes2(terrain3.matrix, individual_decentralized_split_rewards_policy_map3_file, False)
    # peer_aware_decentralized_policy_maker_map3 = MDP_Peer_Aware_Decentralized_policy_maker_twoDBoxes2(terrain3.matrix, peer_aware_decentralized_split_rewards_policy_map3_file, False)
    # peer_listen_decentralized_policy_maker_map3 = MDP_Peer_Listen_Decentralized_policy_maker_twoDBoxes2(terrain3.matrix, peer_listen_decentralized_split_rewards_policy_map3_file, False)

    # quit()

    # define a variable to control the main loop
    running = True

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    pygame.display.set_caption("Boxes")

    # game window centered on start
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    # create world
    # world = World_twoDBoxes2(terrain1, centralized_policy_map1_file)
    # world = World_twoDBoxes2(terrain1, individual_decentralized_split_rewards_policy_map1_file)
    # world = World_twoDBoxes2(terrain1, peer_aware_decentralized_split_rewards_policy_map1_file)
    # world = World_twoDBoxes2(terrain1, peer_listen_decentralized_split_rewards_policy_map1_file)

    # world = World_twoDBoxes2(terrain2, centralized_policy_map2_file)
    # world = World_twoDBoxes2(terrain2, individual_decentralized_split_rewards_policy_map2_file)
    # world = World_twoDBoxes2(terrain2, peer_aware_decentralized_split_rewards_policy_map2_file)
    world = World_twoDBoxes2(terrain2, peer_listen_decentralized_split_rewards_policy_map2_file)
    
    # world = World_twoDBoxes2(terrain3, centralized_policy_map3_file)
    # world = World_twoDBoxes2(terrain3, individual_decentralized_split_rewards_policy_map3_file)
    # world = World_twoDBoxes2(terrain3, peer_aware_decentralized_split_rewards_policy_map3_file)
    # world = World_twoDBoxes2(terrain3, peer_listen_decentralized_split_rewards_policy_map3_file)

    world.render()

    run_states = []

    # main loop
    while running:
        world_update_state = world.update()
        if world_update_state is not None:
            run_states.append(world_update_state)
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

    analyser_map1 = Analyser_twoDBoxes2(terrain1.matrix, run_states)
    # analyser_map2 = Analyser_twoDBoxes2(terrain2.matrix, run_states)
    # analyser_map3 = Analyser_twoDBoxes2(terrain3.matrix, run_states)


if __name__ == "__main__":
    # call the main function
    main()
