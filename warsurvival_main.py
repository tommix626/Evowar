# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:02:14 2021
#the evowar game end to update at version 0.92,instead i want to make this into a no network-need game with different playing rules

this is another game project aim at create a defense-attacking war game

//log
    0.8     start of file
            basic environment
    0.9     cursor invloved
    0.91    eat dots
            player level up system
    0.92    fence block
            font tips
    0.93    change the structure of the code
            adding a framework(gameAgent)
    0.94    adding buildings and bullet
    0.95   trivial uppdates
    0.96    add troops
            inhanced speed
    0.97    troop stategy
    0.98    various troops and controls
            
            
//improvs
    -dot size smaller,circle, dot color brighter,ban red(v0.92)
    -add a fence(v0.8)
    -use cursor to move player(v0.9)
    -blocks outside fence(v0.9)
    -drawing optimise(v0.9x)
    -prob:bullet can't escape the trap of the building(solved)
    -special thanks to wyk for report lots of bugs for the program to improve
    - use a fatherclass function move to create more variable movements(as follow)
    -only at this moment have i realize that in this version of pygame pos doesn't need to be a int
    -troop strategy(v0.97)
    -setting
    -player hp system(v0.97)
    -player rebirth (v0.97)
    -troop sight(v0.97)
    -use arror keys to change kind of troops,and key(1-5) to implement
    -add enemy-type as a parameter(for hptower...)
    -use "enemy tag"/extra_draw instead of distinct color to distinguish enemies from friends
    -items can cross fence
    -draw buffs use towrs enemy to hollow circle
@author: Tom
"""


import sys
import pygame
import random
import math

from cls_player import CLS_Player
from cls_building import CLS_Building
from cls_game_agent import CLS_GameAgent
from global_variables import stgNameList,STRATEGY_NUM,SCREEN_H,SCREEN_W,GRID_SIZE,hpList


'''
I decided to add some consumption to exp for spawning different troops, towers or even respawning 
The current values are as follows
shooting:2 <-- in CLS_Player.shoot_line()
respawning:100 <-- this makes respawning a more of stratagy, but it is up to you, in cls_player.rebirth()
other towers:300 <-- in CLS_GameAgent
troops:500<-- there seems to be exsisting codes, but I failed to find them
the list for storing above numbers are in global_variables.expConsumption
@Ling
'''

'''
Also, I find it IMPOSSIBLE to find the part I need
so I decide to put the classes into different files
hope you can understand
still, you can change the from...import to import to ease further modifications
@Ling
'''





#pygame init
pygame.init()
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
fontScore = pygame.font.Font(None,28)
clock = pygame.time.Clock()
#-----user data-----
#dotList = []
keep_shooting=-1
player = CLS_Player(screen,1)
boss=CLS_Building(screen,[50,50],1,player,9,40,10000)
agent = CLS_GameAgent(screen,player,boss)
boss.totalList=agent.totalList
for i in range(300):
    agent.create_dot()
mouse_x,mouse_y = 0,0

#-----main-----
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #其他鼠标键盘事件
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                agent.build_item("shooter",0,100)
            if event.key==pygame.K_RIGHT:
                agent.build_item("gunner",0,50)
            if event.key==pygame.K_UP:
                agent.build_item("gunner",1,-50)
            if event.key==pygame.K_DOWN:
                agent.build_item("shooter",1,-100)
            if event.key==pygame.K_1:
                agent.build_item("slower",0,0,"range")
            if event.key==pygame.K_2:
                agent.build_item("slower",1,0,"range")
            if event.key==pygame.K_3:
                agent.build_item("poisoner_T",1,0,"range")
            if event.key==pygame.K_4:
                agent.build_item("poisoner_T",0,0,"range")
            if event.key==pygame.K_SPACE:
                flag=1
                while(flag):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        #其他鼠标键盘事件
                        if event.type==pygame.KEYDOWN:
                            if event.key==pygame.K_SPACE:
                                flag=0
                                print(player.aa)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed()
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    if index == 0:
                        print('Pressed LEFT Button!shoot!')
                        keep_shooting=1
                        #agent.pilot.exp-=300
                        #agent.pilot.surspeed(300)
                        #agent.pilot.shoot_line(agent.totalList,agent.bulletList)
                    elif index == 1:
                        print('The mouse wheel Pressed!')
                        agent.pilot.pos=[GRID_SIZE[0]//2,GRID_SIZE[1]//2]
                    elif index == 2:
                        print('Pressed RIGHT Button!')
                        agent.troopstrategy=(agent.troopstrategy+1)%STRATEGY_NUM
        elif event.type == pygame.MOUSEBUTTONUP:
            index = event.button
            if index == 1:
                print("Left up")
                keep_shooting=-1
            elif index == 2:
                print("middle UP")
            elif index == 3:
                print("right UP")
        elif event.type == pygame.MOUSEMOTION:
            #return the X and Y position of the mouse cursor
            pos = pygame.mouse.get_pos()
            agent.pilot.mouse_x = pos[0]
            agent.pilot.mouse_y = pos[1]
            #print("mouse:",mouse_x,mouse_y)
    #屏幕涂黑
    screen.fill((0,0,0))
    #主程序
    agent.action()
    if(keep_shooting>=0):
        if(keep_shooting>=5):
            agent.pilot.shoot_line(agent.totalList,agent.bulletList)
            keep_shooting=0
        else:
            keep_shooting+=1
    #提示字
    img_text = fontScore.render('exp:'+str(agent.pilot.exp),True,(250,250,250))
    screen.blit( img_text ,(10,10))
    img_text = fontScore.render('strategy:'+str(stgNameList[agent.troopstrategy]),True,(250,250,250))
    screen.blit( img_text ,(10,30))
    img_text = fontScore.render('HP:'+str(agent.pilot.hp)+"/"+str(hpList[agent.pilot.lv]),True,(250,250,250))
    screen.blit( img_text ,(10,50))
    for item in agent.towerList[0]+agent.towerList[1]+agent.troopList[0]+agent.troopList[1]:
        scrpos=item.draw(player.fpos,player.pos,2)
        if(scrpos==-1):
            continue
        img_text = fontScore.render('HP:'+str(item.hp),True,(250,250,250))
        screen.blit( img_text ,scrpos)
    scrpos=agent.boss.draw(player.fpos,player.pos,2)
    if(scrpos!=-1):
        img_text = fontScore.render('HP:'+str(agent.boss.hp),True,(250,250,250))
        screen.blit( img_text ,scrpos)
    pygame.display.update()
    clock.tick(100)

