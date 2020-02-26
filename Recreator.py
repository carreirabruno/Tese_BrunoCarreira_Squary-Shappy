import pygame
from Shappy import *
import sys
from World import *
import os
import xml.etree.ElementTree as ET
import numpy as np
import time

settings_array = []
map_design_array = []
A_shappy_pos = []
B_shappy_pos = []
squary_pos = []
game_states = 0

def readXML(filename):
    global game_states
    tree = ET.parse(filename)
    root = tree.getroot()
    for node in root:
        if node.tag == "settings":
            for child in node:
                if child.tag == "TimeStamp_tick":
                    settings_array.append(float(child.text))
                if child.tag == "Terrain_map":
                    settings_array.append(child.text)
                if child.tag == "Screen_ratio":
                    settings_array.append(int(child.text))
        if node.tag == "map_design":
            for child in node:
                string = str(child.text).translate({ord(i): None for i in '\'<rect>,()'})
                string_list = np.array(string.split(" "))
                res = string_list.astype(np.int)
                map_design_array.append(res)
        if node.tag == "game_state":
            for child in node:
                if child.tag == "Timestamp":
                    game_states = int(child.text)
                if child.tag == "shappys":
                    for shappy in child:
                        if shappy.tag == "A":
                            for information in shappy:
                                if information.tag == "Current_Rect":
                                    string = str(information.text).translate({ord(i): None for i in '\'<rect>,()'})
                                    string_list = np.array(string.split(" "))
                                    res = string_list.astype(np.int)
                                    A_shappy_pos.append(res)
                        if shappy.tag == "B":
                            for information in shappy:
                                if information.tag == "Current_Rect":
                                    string = str(information.text).translate({ord(i): None for i in '\'<rect>,()'})
                                    string_list = np.array(string.split(" "))
                                    res = string_list.astype(np.int)
                                    B_shappy_pos.append(res)
                if child.tag == "squary":
                    string = str(child.text).translate({ord(i): None for i in '\'<rect>,()'})
                    string_list = np.array(string.split(" "))
                    res = string_list.astype(np.int)
                    squary_pos.append(res)

def simulate():
    #readXML(filename)

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
    terrain_file = settings_array[1]
    update_time = settings_array[0]
    display_on = 1
    #create world
    world = World(10, 5, "single", update_time, terrain_file, num_directions, learning_rate, epochs, display_on)


    # #create world
    # world = World(settings_array[1], settings_array[2], 5, "single", update_time)

    for item in range(len(map_design_array)):
        wall = Wall("wall", world.screen, map_design_array[item][0], map_design_array[item][1],
                    map_design_array[item][2], map_design_array[item][3])
        world.wall_group.add(wall)

    for s in world.shappy_group:
        if s.name == "A":
            shappyA = s
        elif s.name == "B":
            shappyB = s
    for s in world.squary_group:
        squary = s

    world.render()

    lastTime = time.time()
    game_iterations = 1

    # main loop
#    while running:
    while game_iterations <= game_states:

        if time.time() - lastTime > settings_array[0]:

            shappyA.rect = pygame.Rect(A_shappy_pos[game_iterations][0], A_shappy_pos[game_iterations][1],
                                       A_shappy_pos[game_iterations][2], A_shappy_pos[game_iterations][3])
            shappyB.rect = pygame.Rect(B_shappy_pos[game_iterations][0], B_shappy_pos[game_iterations][1],
                                       B_shappy_pos[game_iterations][2], B_shappy_pos[game_iterations][3])
            squary.rect = pygame.Rect(squary_pos[game_iterations][0], squary_pos[game_iterations][1],
                                      squary_pos[game_iterations][2], squary_pos[game_iterations][3])

            world.render()

            game_iterations += 1
            lastTime = time.time()

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                break
    pygame.quit()

def main(filename):
    readXML(filename)
    simulate()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main(sys.argv[1])
