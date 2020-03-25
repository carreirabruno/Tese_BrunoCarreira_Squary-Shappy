import pygame
import os
from oneDBoxesScenario.Collaborator_oneDBoxes import *
from oneDBoxesScenario.MDP_Centralized_policy_maker_oneDBoxes import *
from oneDBoxesScenario.MDP_Decentralized_policy_maker_oneDBoxes import *
from oneDBoxesScenario.World_oneDBoxes import *
from oneDBoxesScenario.Terrain_oneDBoxes import *
from oneDBoxesScenario.Policy_comparator_oneDBoxes import *
import winsound

def main():

    base_policy2_file = "oneDBoxes_MDP_base_policy2.pickle"
    base_policy3_file = "oneDBoxes_MDP_base_policy3.pickle"

    individual_base_policy2_file = "oneDBoxes_MDP_base_policy2_individual.pickle"

    terrain2 = Terrain_oneDBoxes("oneDBoxes_map2.txt")
    terrain3 = Terrain_oneDBoxes("oneDBoxes_map3.txt")


    #create the policy
    #policy_maker_map2 = MDP_Centralized_policy_maker_oneDBoxes(terrain2.matrix, base_policy2_file)
    # policy_maker_map3 = MDP_Centralized_policy_maker_oneDBoxes(terrain3.matrix, base_policy3_file)

    # decentralized_policy_maker = MDP_Decentralized_policy_maker_oneDBoxes(terrain2.matrix, individual_base_policy2_file)

    #winsound.Beep(600, 500)

    # define a variable to control the main loop
    running = True

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    pygame.display.set_caption("Boxes")

    # game window centered on start
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    #create world
    world = World_oneDBoxes(terrain2, individual_base_policy2_file, "Decentralized")

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
            #policy_comparator.receive_world_simulation_run(world.simulation_run_states)
            running = False

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #policy_comparator.receive_world_simulation_run(world.simulation_run_states)
                running = False
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

    #Policy_comparator_oneDBoxes([collaborative_policy_file, non_collaborative_policy_file]). \
     #   receive_world_simulation_run2(world.simulation_run_states)

if __name__ == "__main__":
    # call the main function
    main()
