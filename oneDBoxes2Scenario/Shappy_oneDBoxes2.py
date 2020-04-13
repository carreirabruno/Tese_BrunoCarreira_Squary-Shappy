from World import *
import math
from itertools import *
import sys
import numpy
import copy

numpy.set_printoptions(threshold=sys.maxsize)


def get_center(sprite):
    return sprite.rect.x + sprite.rect.width / 2, sprite.rect.y + sprite.rect.height / 2


class Shappy_oneDBoxes2(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, world, color, current_map, screen_width, screen_height,
                 auto, policy, type_of_policy, current_state):

        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.old_x_pos = x_pos
        self.old_y_pos = y_pos
        self.world = world
        self.current_map = current_map
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.auto = auto
        self.policy = policy
        self.type_of_policy = type_of_policy
        self.current_state = current_state

        self.color = color

        self.dir_vector = []

        self.calculate = False
        self.next_boxes = []
        self.current_box = math.inf
        self.next_box_x = math.inf

        if self.color == 3:
            self.image = pygame.image.load("../Images/20_20_Blue_Square.png")
        elif self.color == 4:
            self.image = pygame.image.load("../Images/20_20_Red_Square.png")
        else:
            print("Unknown colour number: ", self.color)

        x_size, y_size = self.image.get_rect().size
        self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.dir = (x_pos, y_pos)

        self.time_interval = time.time()

        self.current_state = []

        # for line in policy:
        #     print(self.color, line)
        # print()

        self.I_Know = False

    def update(self, current_state):
        self.current_state = copy.deepcopy(current_state)
        if not self.auto:
            self.calculate = False
            keys = pygame.key.get_pressed()
            if self.color == 3:
                if keys[pygame.K_a]:
                    self.lefty()
                if keys[pygame.K_d]:
                    self.righty()
            elif self.color == 4:
                if keys[pygame.K_LEFT]:
                    self.lefty()
                if keys[pygame.K_RIGHT]:
                    self.righty()
        elif self.auto:
            self.auto_movement(self.type_of_policy)

        self.time_interval = time.time()

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

        self.dir = (self.x_pos - self.old_x_pos, self.y_pos - self.old_y_pos)

        self.old_x_pos = self.x_pos
        self.old_y_pos = self.y_pos

        return self.current_state

    def lefty(self):
        if self.current_map[(int(self.x_pos / self.world.screen_ratio) - 1)] != 1:

            self.x_pos -= 1 * self.world.screen_ratio

            if self.current_map[int(self.x_pos / self.world.screen_ratio)] == 2:
                self.world.box_group_remove(int(self.x_pos / self.world.screen_ratio),
                                            int(self.y_pos / self.world.screen_ratio))

                self.current_state.remove(int(self.x_pos / self.world.screen_ratio))

    def righty(self):
        if self.current_map[(int(self.x_pos / self.world.screen_ratio) + 1)] != 1:

            self.x_pos += 1 * self.world.screen_ratio

            if self.current_map[int(self.x_pos / self.world.screen_ratio)] == 2:
                self.world.box_group_remove(int(self.x_pos / self.world.screen_ratio),
                                            int(self.y_pos / self.world.screen_ratio))

                self.current_state.remove(int(self.x_pos / self.world.screen_ratio))

    def communicaty(self):
        for shappy in self.world.shappy_group:
            if shappy.color != self.color:
                shappy.I_Know = True
        # print(self.color, "Communicated")


    def auto_movement(self, type):
        if type == "centralized":
            actions = -1
            for state in self.policy:
                equal = True
                for i in range(len(state[0])):
                    if len(self.current_state) != len(state[0]) or self.current_state[i] != state[0][i]:
                        equal = False
                if equal:
                    actions = np.argmax(state[1])
                    break

            if self.color == 3:
                if actions == 0 or actions == 1:
                    pass
                elif actions == 2 or actions == 3 or actions == 4:
                    self.lefty()
                elif actions == 5 or actions == 6 or actions == 7:
                    self.righty()
                self.current_state[0] = int(self.x_pos / self.world.screen_ratio)

            elif self.color == 4:
                if actions == 2 or actions == 5:
                    pass
                elif actions == 0 or actions == 3 or actions == 6:
                    self.lefty()
                elif actions == 1 or actions == 4 or actions == 7:
                    self.righty()
                self.current_state[1] = int(self.x_pos / self.world.screen_ratio)

        elif type == "decentralized":
            self.current_state.remove(self.current_state[0])
            self.current_state[0] = int(self.x_pos/self.world.screen_ratio)

            actions = -1
            for state in self.policy:
                equal = True
                for i in range(len(state[0])):
                    if len(self.current_state) != len(state[0]) or self.current_state[i] != state[0][i]:
                        equal = False
                if equal:
                    actions = np.argmax(state[1])
                    break
            if actions == 0:
                pass
            elif actions == 1:
                self.lefty()
            elif actions == 2:
                self.righty()

            self.current_state[0] = int(self.x_pos / self.world.screen_ratio)

        elif type == "peer_aware_decentralized":
            if self.color == 3:
                # for line in self.policy:
                #     print("  3  ", line)
                # print(self.current_state)
                pass
            # elif self.color == 4:
            #     # for line in self.policy:
            #     #     print("  4  ", line)
            #     # quit()
            #     self.current_state[1] = self.current_state[0]
            #     self.current_state[0] = int(self.x_pos/self.world.screen_ratio)
            #     # print(self.current_state)

            actions = -1
            for state in self.policy:
                equal = True
                for i in range(len(state[0])):
                    if len(self.current_state) != len(state[0]) or self.current_state[i] != state[0][i]:
                        equal = False
                if equal:
                    actions = np.argmax(state[1])
                    #print(self.color, self.current_map, self.current_state, state)
                    break

            if actions == 0:
                pass
            elif actions == 1:
                self.lefty()
            elif actions == 2:
                self.righty()

            if self.color == 3:
                # print(actions)
                self.current_state[0] = int(self.x_pos / self.world.screen_ratio)
            elif self.color == 4:
                # self.current_state[0] = self.current_state[1]
                self.current_state[1] = int(self.x_pos / self.world.screen_ratio)

        elif type == "peer_communication_decentralized":
            if self.color == 3 and not self.I_Know:
                # for pol in self.policy:
                #     if np.argmax(pol[1]) == 3:
                #         print(" 3 -- ", pol)
                self.current_state[1] = -1
            elif self.color == 4 and not self.I_Know:
                # for pol in self.policy:
                #     if np.argmax(pol[1]) == 3:
                #         print(" 4 -- ", pol)
                self.current_state[0] = -1
                # quit()

            print(self.color, self.current_state)

            actions = -1
            for state in self.policy:
                equal = True
                for i in range(len(state[0])):
                    if len(self.current_state) != len(state[0]) or self.current_state[i] != state[0][i]:
                        equal = False
                if equal:
                    actions = np.argmax(state[1])
                    # print(self.color, self.current_map, self.current_state, state)
                    break

            print(actions)

            if actions == 0:
                pass
            elif actions == 1:
                self.lefty()
            elif actions == 2:
                self.righty()
            elif actions == 3:
                if self.color == 1:
                    pass
                else:
                    self.communicaty()

            if self.color == 3:
                # print(actions)
                self.current_state[0] = int(self.x_pos / self.world.screen_ratio)
            elif self.color == 4:
                # self.current_state[0] = self.current_state[1]
                self.current_state[1] = int(self.x_pos / self.world.screen_ratio)

            # print()
