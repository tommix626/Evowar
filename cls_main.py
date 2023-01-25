from global_variables import SCREEN_H, SCREEN_W, SCREEN_SIZE
from calc import cal_dist,cal_scrpos
import pygame
import math


BULLET_RAD_INIT,BULLET_DUR_INIT,BULLET_ATK_INIT,BULLET_SPD_INIT=3,80,50,3
SIGHT_RAD_INIT=min(SCREEN_SIZE)//2.2
class CLS_item(object):
    def __init__(self,screen,rad,pos,speed,hp,color,atkrange,atk,interval,side,polySideNum):
        self.rad=rad
        self.pos=pos
        self.speed=speed
        self.hp=hp
        self.surface=screen
        self.color=color
        self.dcolor=(255-color[0],255-color[1],255-color[2])
        self.atkrange=atkrange
        self.atk=atk
        self.interval=interval
        self.side=side
        self.bltrad=BULLET_RAD_INIT
        self.bltdur=BULLET_DUR_INIT
        self.bltatk=atk
        self.bltspd=BULLET_SPD_INIT
        self.sightrad=SIGHT_RAD_INIT
        self.poly=polySideNum
        self.buffList=[]#for rebuffing contain inverse-buff affect and time to release |("atk",3,20,BuildingX)->BuildingX give this item a +3atk buff lasting 20 frame |
        self.buffatk,self.buffspeed=0,0
        self.bgcolor=None
        return
    def draw(self,fpos,ppos,tag=0):#use player Position to draw self
        if(tag==1):
            print("draw")
        dx,dy=cal_scrpos(self.pos,fpos,ppos)
        if(dx+self.rad<0 or dx-self.rad>SCREEN_W or dy+self.rad<0 or dy-self.rad>SCREEN_H):
            if(tag==1):
                print("out of range")
            return -1
        if(tag==0):
            pygame.draw.circle(self.surface,self.color,[dx,dy],self.rad,0)
            self.draw_extras(dx,dy,self.poly)
        elif(tag==2):
            if(dx<0 or dx>SCREEN_W or dy<0 or dy>SCREEN_H):
                return -1
            return(dx-self.rad,dy+self.rad)
        if(tag==1):
            print("success",self.color,dx,dy)
        return
    def draw_extras(self,x,y,sideNum=0):#FIXME can be reload to mark different buildings (will consider to use it to distinct between enemy and self)
        pointList=[]
        r=self.rad/2
        if(sideNum==0):
            pygame.draw.circle(self.surface,self.dcolor,[x,y],r,0)
            return
        if(sideNum==-1):
            return
        for i in range(sideNum):
            ang=2*math.pi/sideNum*i
            pointList.append((x+r*math.cos(ang),y+r*math.sin(ang)))
        pygame.draw.polygon(self.surface,self.dcolor,pointList,0)
        return
    def draw_background(self,dx,dy):#for special towers
        if(self.bgcolor==None):
            return
        pygame.draw.circle(self.surface,self.bgcolor,[dx,dy],self.atkrange,0)
        return
    def check_buff(self):
        self.buffatk,self.buffspeed=0,0
        #one building can only cause one buff of a kind
        for i in range(len(self.buffList)-1):
            for j in range(i+1,len(self.buffList)):
                if(self.buffList[i][3]==self.buffList[j][3] and self.buffList[i][0]==self.buffList[j][0]):
                    self.buffList[i][2]=-1
        for buff in self.buffList:
            print(buff[2])
            if(buff[2]<=0):
                continue
            buff[2]-=1
            if(buff[0]=="atk+"):
                self.buffatk+=buff[1]
            elif(buff[0]=="atk-"):
                self.buffatk-=buff[1]
            elif(buff[0]=="speed-"):
                self.buffspeed-=buff[1]
            elif(buff[0]=="speed+"):
                self.buffspeed+=buff[1]
        for buff in self.buffList:
            print(buff[2])
            if(buff[2]<=0):
                self.buffList.remove(buff)
                continue
            buff[2]-=1
        #print("buff:",self.buffatk,self.buffspeed)