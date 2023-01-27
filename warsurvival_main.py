import sys
import pygame


from cls_player import CLS_Player
from cls_building import CLS_Building
from cls_game_agent import CLS_GameAgent
from renderer import Renderer
from global_variables import (
    stgNameList,
    STRATEGY_NUM,
    SCREEN_H,
    SCREEN_W,
    GRID_SIZE,
    hpList,
)


# pygame init
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()
# -----user data-----
# dotList = []
keep_shooting = -1
renderer = Renderer(screen)
player = CLS_Player(renderer, 1)
boss = CLS_Building(renderer, [50, 50], 1, player, 9, 40, 10000)
agent = CLS_GameAgent(renderer, player, boss)
boss.totalList = agent.totalList
for i in range(300):
    agent.create_dot()
mouse_x, mouse_y = 0, 0

# -----main-----
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 其他鼠标键盘事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                agent.build_item("shooter", 0, 100)
            if event.key == pygame.K_RIGHT:
                agent.build_item("gunner", 0, 50)
            if event.key == pygame.K_UP:
                agent.build_item("gunner", 1, -50)
            if event.key == pygame.K_DOWN:
                agent.build_item("shooter", 1, -100)
            if event.key == pygame.K_1:
                agent.build_item("slower", 0, 0, "range")
            if event.key == pygame.K_2:
                agent.build_item("slower", 1, 0, "range")
            if event.key == pygame.K_3:
                agent.build_item("poisoner_T", 1, 0, "range")
            if event.key == pygame.K_4:
                agent.build_item("poisoner_T", 0, 0, "range")
            if event.key == pygame.K_m:
                agent.display_map()
            if event.key == pygame.K_SPACE:
                flag = 1
                while flag:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        # 其他鼠标键盘事件mmmmmmm
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                flag = 0
                                print(player.aa)
                                # BUG here FIXME
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed()
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    if index == 0:
                        print("Pressed LEFT Button!shoot!")
                        keep_shooting = 1
                        # agent.pilot.exp-=300
                        # agent.pilot.surspeed(300)
                        # agent.pilot.shoot_line(agent.totalList,agent.bulletList)
                    elif index == 1:
                        print("The mouse wheel Pressed!")
                        agent.pilot.pos = [GRID_SIZE[0] // 2, GRID_SIZE[1] // 2]
                    elif index == 2:
                        print("Pressed RIGHT Button!")
                        agent.troopstrategy = (agent.troopstrategy + 1) % STRATEGY_NUM
        elif event.type == pygame.MOUSEBUTTONUP:
            index = event.button
            if index == 1:
                print("Left up")
                keep_shooting = -1
            elif index == 2:
                print("middle UP")
            elif index == 3:
                print("right UP")
        elif event.type == pygame.MOUSEMOTION:
            # return the X and Y position of the mouse cursor
            pos = pygame.mouse.get_pos()
            agent.pilot.mouse_x = pos[0]
            agent.pilot.mouse_y = pos[1]
            # print("mouse:",mouse_x,mouse_y)
    # 屏幕涂黑
    screen.fill((0, 0, 0))
    # 主程序
    agent.action()
    if keep_shooting >= 0:
        if keep_shooting >= 5:
            agent.pilot.shoot_line(agent.totalList, agent.bulletList)
            keep_shooting = 0
        else:
            keep_shooting += 1
    # 提示字
    renderer.draw_text(player, agent)
    pygame.display.update()
    clock.tick(100)
