import xml.etree.cElementTree as ET
import time
import os
import datetime
import xml.dom.minidom
from World import *

datetime_object = datetime.datetime.now()
filename = ("logs/" + datetime_object.strftime("DATE_%d-%m-%Y___TIME_%H-%M-%S") + ".xml")

def createNewLogFile(world):
    path = "logs"
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

    root = ET.Element("root")
    settings = ET.SubElement(root, "settings")
    map_design = ET.SubElement(root, "map_design")

    ET.SubElement(settings, "TimeStamp_tick").text = str(world.update_time)
    ET.SubElement(settings, "Terrain_map").text = str(world.terrain_file)
    ET.SubElement(settings, "Screen_ratio").text = str(world.screen_ratio)

    for wall in world.wall_group:
        ET.SubElement(map_design, wall.name + "-Current_Rect").text = str(wall.rect)

    tree = ET.ElementTree(root)

    tree.write(filename)
    addGameState(world, 0)


def addGameState(world, iteration):
    tree = ET.ElementTree(file=filename)
    root = tree.getroot()
    game_state = ET.SubElement(root, "game_state")

    ET.SubElement(game_state, "Timestamp").text = str(iteration)
    shappys = ET.SubElement(game_state, "shappys")
    for shappy in world.shappy_group:
        users = ET.SubElement(shappys, shappy.name)
       # ET.SubElement(users, "Color").text = str(shappy.color)
        ET.SubElement(users, "Direction").text = str(shappy.dir_vector)
        ET.SubElement(users, "Current_Rect").text = str(shappy.rect)

    for squary in world.squary_group:
       # users = ET.SubElement(squarys, "Greeny")
       # ET.SubElement(users, "Color").text = str(shappy.color)
       # ET.SubElement(users, "Current_Rect").text = str(squary.rect)
       ET.SubElement(game_state, "squary").text = str(squary.rect)
    tree.write(filename)



def prettyXML(): ##############Re-write file with pretty XML################## Nao usado
    file = open(filename, 'r')
    xml_string = file.read()
    file.close()
    parsed_xml = xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = parsed_xml.toprettyxml()

    file = open(filename, 'w')
    file.write(pretty_xml_as_string)
    file.close()