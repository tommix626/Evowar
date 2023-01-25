import random,pygame
from global_variables import SCREEN_SIZE,SCREEN_W,SCREEN_H,DOT_R_RANGE,GRID_SIZE

class CLS_Dot(object):
    def __init__(self,screen,pos,rad,color=(200,200,200)):
        self.rad = rad
        self.color=color
        self.pos=pos# real position on the grid
        self.surface = screen
        self.pts = self.rad*2
    def draw(self,fpos,ppos):#use player Position(ppos) to draw self
        dx,dy=self.pos[0]-ppos[0]+fpos[0],self.pos[1]-ppos[1]+fpos[1]
        if(dx+self.rad<0 or dx-self.rad>SCREEN_W or dy+self.rad<0 or dy-self.rad>SCREEN_H):
            return
        pygame.draw.circle(self.surface,self.color,[dx,dy],self.rad,0)
        return
    def rebirth(self):
        self.pos[0]=random.randint(0+DOT_R_RANGE[1],GRID_SIZE[0]-DOT_R_RANGE[1])
        self.pos[1]=random.randint(0+DOT_R_RANGE[1],GRID_SIZE[1]-DOT_R_RANGE[1])
        self.rad =random.randint(DOT_R_RANGE[0],DOT_R_RANGE[1])
        self.pts = self.rad*2
        self.color=(random.randint(50,150),random.randint(100,255),random.randint(100,255))
