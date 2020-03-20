import pygame
import os
from oneDBoxesScenario.Collaborator_oneDBoxes import *
from oneDBoxesScenario.MDP_Policy_maker_oneDBoxes import *
from oneDBoxesScenario.World_oneDBoxes import *
from oneDBoxesScenario.Terrain_oneDBoxes import *
from oneDBoxesScenario.Policy_comparator_oneDBoxes import *
import winsound

def main():
    base_policy_file = "oneDBoxes_MDP_base_policy.txt"
    collaborative_policy_file = "oneDBoxes_MDP_collaborative_policy2.txt"
    non_collaborative_policy_file = "oneDBoxes_MDP_non_collaborative_policy2.txt"

    terrain = Terrain_oneDBoxes("oneDBoxes_map2.txt")

    #create the policy
    policy_maker_col = MDP_Policy_maker_oneDBoxes(terrain.matrix, collaborative_policy_file)
    policy_maker_non_col = MDP_Policy_maker_oneDBoxes(terrain.matrix, non_collaborative_policy_file)
    #winsound.Beep(600, 500)

    quit()

    #create the comparator
    #policy_comparator = Policy_comparator_oneDBoxes([collaborative_policy_file, non_collaborative_policy_file])

    # define a variable to control the main loop
    running = True

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    pygame.display.set_caption("Boxes")

    # game window centered on start
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    #create world
    world = World_oneDBoxes(terrain, collaborative_policy_file)

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
            policy_comparator.receive_world_simulation_run(world.simulation_run_states)
            running = False

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                policy_comparator.receive_world_simulation_run(world.simulation_run_states)
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

if __name__ == "__main__":
    # call the main function
    main()
