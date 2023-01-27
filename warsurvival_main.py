import pygame


from mouse_handler import CLS_Mouse_Handler
from cls_player import CLS_Player
from cls_building import CLS_Building
from cls_game_agent import CLS_GameAgent
from renderer import Renderer
from global_variables import (
    SCREEN_H,
    SCREEN_W,
)


# pygame init
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()
# -----user data-----
# dotList = []
shooting_mode = -1
temp = -1
renderer = Renderer(screen)
player = CLS_Player(renderer, 1)
boss = CLS_Building(renderer, [50, 50], 1, player, 9, 40, 10000)
agent = CLS_GameAgent(renderer, player, boss)
mouse_handler = CLS_Mouse_Handler(agent)
boss.totalList = agent.totalList
for i in range(300):
    agent.create_dot()
mouse_x, mouse_y = 0, 0

# -----main-----
while True:
    for event in pygame.event.get():
        temp = mouse_handler.process(event)
        if temp is not None:
            shooting_mode = temp
    # 屏幕涂黑
    screen.fill((0, 0, 0))
    # 主程序
    agent.action()
    if shooting_mode >= 0:
        if shooting_mode >= 5:
            agent.pilot.shoot_line(agent.totalList, agent.bulletList)
            shooting_mode = 0
        else:
            shooting_mode += 1
    # 提示字
    renderer.draw_text(player, agent)
    pygame.display.update()
    clock.tick(100)
