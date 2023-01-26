import pygame
from global_variables import SCREEN_W,SCREEN_H,SCREEN_SIZE,GRID_SIZE,spdList,colorList,radList,atkList,hpList,expList,expConsumption
from cls_bullet import CLS_Bullet
from renderer import Renderer



PLAYER_HP_INIT=1000
class CLS_Player(object):
    def __init__(self,renderer,lv):
        self.speed=[0,0] # instant speed
        self.bspd = 0 # bonus speed-multiplyer
        self.bframe = 0 #bonus frame time
        self.exp = 0
        self.lv = lv
        self.fpos=[SCREEN_W//2,SCREEN_H//2] #always centering(fix pos)
        self.pos=[GRID_SIZE[0]//2,GRID_SIZE[1]//2] #real pos
        #self.surface=scr#this should be deleted after full transfer
        self.renderer=renderer
        self.color=colorList[self.lv]
        self.spdLv = spdList[self.lv] # the speed decrease as player's lv increase
        self.rad=radList[self.lv]
        self.bltatk,self.bltrad,self.bltdur,self.bltspd=atkList[self.lv][0],atkList[self.lv][1],atkList[self.lv][2],atkList[self.lv][3]
        self.hp=hpList[self.lv]
        self.rect = [self.fpos[0]-self.rad//2,self.fpos[1]-self.rad//2,self.rad//1,self.rad//1]
        self.rectcolor=(0,0,0)
        self.mouse_x,self.mouse_y=self.fpos[0],self.fpos[1]
        self.buffList=[]
        self.buffatk,self.buffspeed=0,0
        return

    
    #actionList for one frame----------------------
    def action(self):
        #interaction
        self.spec_check()
        self.check_buff()
        self.move()
        self.lvup()
        #drawing
        self.draw()
        self.redirct(self.mouse_x,self.mouse_y)
        return
    #-----------------------------------------------
    def draw(self):
        self.renderer.draw_player(self)
        
    def move(self):
        if(self.pos[0]+self.speed[0]-self.rad>=0 and self.pos[0]+self.speed[0]+self.rad<=GRID_SIZE[0]):
            self.pos[0]+=self.speed[0]*(self.buffspeed+1)
        if(self.pos[1]+self.speed[1]-self.rad>=0 and self.pos[1]+self.speed[1]+self.rad<=GRID_SIZE[1]):
            self.pos[1]+=self.speed[1]*(self.buffspeed+1)
    def redirct(self,posx,posy):
        dx,dy = posx-self.fpos[0],posy-self.fpos[1]
        dr = (dx*dx+dy*dy)**(1/2)
        if(dr<=20):#if too close
            dr=20
        self.speed[0],self.speed[1] = (dx/dr*(self.spdLv+self.bspd))//0.001/1000,(dy/dr*(self.spdLv+self.bspd))//0.001/1000
        return
    def lvup(self):
        #check for abilities upgrade
        if(self.hp>hpList[self.lv]):
            self.hp=hpList[self.lv]
        elif(self.hp<0):
            self.rebirth()
        for i in range(0,len(expList)):
            standard = expList[i]
            if(standard<=self.exp and self.lv<(i+1)):
                self.lv = i+1
                self.spdLv = spdList[self.lv]
                self.rad=radList[self.lv]
                self.color=colorList[self.lv]
                self.rect = [self.fpos[0]-self.rad//2,self.fpos[1]-self.rad//2,self.rad//1,self.rad//1]
                self.bltatk,self.bltrad,self.bltdur,self.bltspd=atkList[self.lv][0],atkList[self.lv][1],atkList[self.lv][2],atkList[self.lv][3]
                return
    def surspeed(self,frameNum,reset=0):#speedup for a certain frames
        if(reset):
            self.bspd = 0
            return
        self.bframe += frameNum
        self.bspd = 3
        return
    def spec_check(self):#special ability checks
        self.bframe-=1
        if(self.bframe<0):
            self.bframe=0
            self.surspeed(-1,1)#reset surplus speed
        return
    def shoot_line(self,ttList,bulletList):# shoot a bullet to where the player faces
        tspd=[self.speed[0]*self.bltspd,self.speed[1]*self.bltspd]
        tpos=[self.pos[0],self.pos[1]]
        bullet = CLS_Bullet(self.renderer,self,self.bltrad,self.bltdur,tpos,0,tspd,0,self.bltatk+self.buffatk,ttList,0)
        bulletList.append(bullet)
        #-n exp per fire
        self.exp=self.exp-expConsumption[0]
        return
    def rebirth(self):
        self.pos=[GRID_SIZE[0]//2,GRID_SIZE[1]//2]
        self.lv=1
        self.color=colorList[self.lv]
        self.spdLv = spdList[self.lv] # the speed decrease as player's lv increase
        self.rad=radList[self.lv]
        self.bltatk,self.bltrad,self.bltdur,self.bltspd=atkList[self.lv][0],atkList[self.lv][1],atkList[self.lv][2],atkList[self.lv][3]
        self.hp=hpList[self.lv]

        #mess up with this bit
        if self.exp>=expConsumption:
            self.exp=self.exp-expConsumption[1]
        else:
            self.exp=0
            
        self.rectcolor=(0,0,100)#marking
        self.rect = [self.fpos[0]-self.rad//2,self.fpos[1]-self.rad//2,self.rad//1,self.rad//1]
    def check_buff(self):
        self.buffatk,self.buffspeed=0,0
        #one building can only cause one buff
        for i in range(len(self.buffList)-1):
            for j in range(i+1,len(self.buffList)):
                if(self.buffList[i][3]==self.buffList[j][3] and self.buffList[i][0]==self.buffList[j][0]):
                    self.buffList[i][2]=-1
                    break
        #print("\n1.",self.buffList)
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
        #print("2.",self.buffList,end="\n\n")