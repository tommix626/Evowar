from global_variables import STRATEGY_NUM, GRID_SIZE

import pygame
import sys


class Mouse_Handler:
    def __init__(self, agent):
        self.agent = agent

    def process(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        match (event.type):
            case (pygame.KEYDOWN):
                match (event.key):
                    case (pygame.K_LEFT):
                        self.agent.build_item("shooter", 0, 100)
                        return
                    case (pygame.K_RIGHT):
                        self.agent.build_item("gunner", 0, 50)
                        return
                    case (pygame.K_UP):
                        self.agent.build_item("gunner", 1, -50)
                        return
                    case (pygame.K_DOWN):
                        self.agent.build_item("shooter", 1, -100)
                        return
                    case (pygame.K_1):
                        self.agent.build_item("slower", 0, 0, "range")
                        return
                    case (pygame.K_2):
                        self.agent.build_item("slower", 1, 0, "range")
                        return
                    case (pygame.K_3):
                        self.agent.build_item("poisoner_T", 1, 0, "range")
                        return
                    case (pygame.K_4):
                        self.agent.build_item("poisoner_T", 0, 0, "range")
                        return
                    # pause the player
                    case (pygame.K_LALT):
                        self.agent.pilot.halt()
                    # Render BIG map
                    case (pygame.K_m):
                        self.agent.display_map()
                        return
                    # Pause and continue funtionality
                    case (pygame.K_SPACE):
                        self.agent.inPause = 1
                        while self.agent.inPause == 1:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if (
                                    event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_SPACE
                                ):
                                    self.agent.inPause = -1
                                    return
            case (pygame.MOUSEBUTTONDOWN):
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            print("Pressed LEFT Button!shoot!")
                            return 1
                            # self.agent.pilot.exp-=300
                            # self.agent.pilot.surspeed(300)
                            # self.agent.pilot.shoot_line(self.agent.totalList,self.agent.bulletList)
                        elif index == 1:
                            print("The mouse wheel Pressed!")
                            self.agent.pilot.pos = [
                                GRID_SIZE[0] // 2,
                                GRID_SIZE[1] // 2,
                            ]
                            return
                        elif index == 2:
                            print("Pressed RIGHT Button!")
                            self.agent.troopstrategy = (
                                self.agent.troopstrategy + 1
                            ) % STRATEGY_NUM
                            return
            case (pygame.MOUSEBUTTONUP):
                index = event.button
                if index == 1:
                    print("Left up")
                    return -1
                elif index == 2:
                    print("middle UP")
                    return
                elif index == 3:
                    print("right UP")
                    return
            case (pygame.MOUSEMOTION):
                pos = pygame.mouse.get_pos()
                self.agent.pilot.mouse_x = pos[0]
                self.agent.pilot.mouse_y = pos[1]
                return
