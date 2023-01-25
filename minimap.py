import pygame
from global_variables import SCREEN_W,SCREEN_H,GRID_SIZE
'''
2023/1/25
the minymap class is used inside the cls game agent
you can draw the minymap at the right top
@Ling
'''
class MinyMap:
    def __init__(self,gameAgent,screen):
        self.gameAgent=gameAgent
        self.dotList=[]
        self.troopList=[[],[]]
        self.towerList=[[],[]]
        self.playerLoc=[]
        self.surface=screen

        self.y_len=int(SCREEN_H/5)
        self.x_len=int(self.y_len/GRID_SIZE[1]*GRID_SIZE[0])
        self.r=GRID_SIZE[1]/self.y_len
        #this makes no difference in 2500x2500
    def sync(self):
        self.dotList=self.gameAgent.dotList
        self.troopList=self.gameAgent.troopList
        self.towerList=self.gameAgent.towerList
        self.playerLoc=self.gameAgent.pilot.pos
    def draw_background(self):
        #the difference of a pixel is unnoticable
        pygame.draw.rect(self.surface,(255,255,255),(SCREEN_W-self.x_len-3,0,self.x_len+2,self.y_len+2))
        pygame.draw.rect(self.surface,(0,0,0),(SCREEN_W-self.x_len-2,1,self.x_len,self.y_len))
    def draw(self,x,y,radius,color): 
        """
        x= real x
        y= real y
        color=(r,g,b)
        """
        fx= SCREEN_W-self.x_len+int(x/self.r)
        fy=int(y/self.r)
        pygame.draw.circle(self.surface,color,(fx,fy),radius)
        #print(fx,fy)
    def draw_main(self):
        self.draw_background()
        for dot in self.dotList:
            self.draw(dot.pos[0],dot.pos[1],1,(100,100,100))
        self.draw(self.playerLoc[0],self.playerLoc[1],3,(0,0,255))
        #self in blue, enemy in red
        for troop in self.troopList[0]:
            self.draw(troop.pos[0],troop.pos[1],1,(100,100,255))
        for troop in self.towerList[1]:
            self.draw(troop.pos[0],troop.pos[1],1,(255,100,0))
        for tower in self.towerList[0]:
            self.draw(tower.pos[0],tower.pos[1],2,(100,100,255))
        for tower in self.troopList[1]:
            self.draw(tower.pos[0],tower.pos[1],2,(255,100,0))
    