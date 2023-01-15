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
#globals
SCREEN_W,SCREEN_H=1000, 600
SCREEN_SIZE = [SCREEN_H,SCREEN_W]
GRID_SIZE = [2500,2500]
FENCE_COLOR=(150,150,200)
DOT_R_RANGE = [5,15] # the range of the dot's radius


#needed to plan for more upgrades
radList=[-1,10,20,30,40,50]#radius of different levels
spdList=[-1,3,2.75,2.5,2.25,2]#speed of different levels
expList=[-1,300,500,1000,2000,1000000]# exp needed for different levels | <300 lv1 || 300-500 lv2 || 500-1000 lv3 |
colorList=[-1,(255,255,255),(255,200,200),(255,150,150),(255,100,100),(255,70,70)]
atkList=[[-1,-1,-1,-1],[20,8,200,3],[40,9,250,4],[60,10,300,5],[80,15,400,6],[100,20,600,7]] #[atk,rad,dur,spd]
hpList=[-10000,1000,1500,2000,3000,10000]

def cal_dist(pos1,pos2):#calulate the distance between two point
    distance = (pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2
    return distance
def cal_speed(pos1,pos2,ratio):#calculate the needed x-y speed (pos1 --> pos2) satisfy speedx^2+speedy^2=ratio^2 |speed|=ratio
    dr = (cal_dist(pos1,pos2))**(1/2)+0.001
    dx,dy=pos2[0]-pos1[0],pos2[1]-pos1[1]
    speed=[dx*ratio/dr//0.001/1000,dy*ratio/dr//0.001/1000]
    return speed
def cal_scrpos(pos,fpos,ppos):
    return pos[0]-ppos[0]+fpos[0],pos[1]-ppos[1]+fpos[1]

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
            

PLAYER_HP_INIT=1000
class CLS_Player(object):
    def __init__(self,scr,lv):
        self.speed=[0,0] # instant speed
        self.bspd = 0 # bonus speed-multiplyer
        self.bframe = 0 #bonus frame time
        self.exp = 0
        self.lv = lv
        self.fpos=[SCREEN_W//2,SCREEN_H//2] #always centering(fix pos)
        self.pos=[GRID_SIZE[0]//2,GRID_SIZE[1]//2] #real pos
        self.surface=scr
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
        pygame.draw.circle(self.surface,self.color,self.fpos,self.rad,0)
        pygame.draw.rect(self.surface,self.rectcolor,self.rect,2)
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
        bullet = CLS_Bullet(self.surface,self,self.bltrad,self.bltdur,tpos,0,tspd,0,self.bltatk+self.buffatk,ttList,0)
        bulletList.append(bullet)
        return
    def rebirth(self):
        self.pos=[GRID_SIZE[0]//2,GRID_SIZE[1]//2]
        self.lv=1
        self.color=colorList[self.lv]
        self.spdLv = spdList[self.lv] # the speed decrease as player's lv increase
        self.rad=radList[self.lv]
        self.bltatk,self.bltrad,self.bltdur,self.bltspd=atkList[self.lv][0],atkList[self.lv][1],atkList[self.lv][2],atkList[self.lv][3]
        self.hp=hpList[self.lv]
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

class CLS_Bullet(CLS_item):
    def __init__(self,screen,player,rad,duration,pos,flag,spd,tgt,atk,totalList=0,selfidx=-1):# for linear: spd is a tuple tgt=0,need totalList,selfidx is index of self in totalList that should not be a target
        self.rad=rad
        self.duration=duration
        self.mode=flag
        self.pos=pos
        self.atk=atk
        self.pilot=player#use for draw self
        self.surface=screen
        self.color=(0,255,0)
        self.poly=-1
        self.bgcolor=None
        if(flag):
            self.target=tgt
            self.spdratio=spd
            self.redirect()
        else:
            self.speed=spd
            self.idx=selfidx
            self.targetList=totalList
        self.show=1
        return
    def action(self):
        if(self.show==0):
            return
        self.duration-=1
        if(self.duration<0):
            self.show=0
            return
        self.bulletmove()
        self.draw(self.pilot.fpos,self.pilot.pos,0)
        return
    def bulletmove(self):
        if(self.mode):# target at one
            self.redirect()
            if(cal_dist(self.pos,self.target.pos)<=(self.rad+self.target.rad)**2):
                self.target.hp-=self.atk
                self.show=0
        else:# taarget for all
            for i in range(len(self.targetList)):
                if(i==self.idx):
                    continue
                for j in range(len(self.targetList[i])):
                    for target in self.targetList[i][j]:
                        if(cal_dist(self.pos,target.pos)<(self.rad+target.rad)**2):
                            target.hp-=self.atk//5
        self.pos[0]+=self.speed[0]
        self.pos[1]+=self.speed[1]
        return
    def redirect(self):
        self.speed = cal_speed(self.pos,self.target.pos,self.spdratio)
        return


class CLS_Building(CLS_item):
    def __init__(self,screen,pos,side,player,polySideNum=-1,rad=10,hp=1000,atkrange=200,atk=10,interval=30):
        color=(255*side,0,255*(1-side))# color change according to side
        super().__init__(screen,rad,pos,[0,0],hp,color,atkrange,atk,interval,side,polySideNum)
        self.cd=interval #cd decrease and reset with time; interval is a constant
        self.pilot = player
        self.bltdur=self.atkrange//self.bltspd*1.1
        return
    def action(self,ttList,bulletList):#hero: player/boss depend on which side this building is on
        self.cd-=1
        self.check_buff()
        self.tgtList=ttList[1-self.side][0]+ttList[2][1-self.side]+ttList[3][1-self.side]# hero+troop+tower enemyList
        self.shoot(self.tgtList,bulletList)# attack enemy
        self.draw(ttList[0][0][0].fpos,ttList[0][0][0].pos)#self.totalList[0][0][0] is player
        return
    def shoot(self,tgtList,bulletList):
        if(self.cd>0):
            return
        self.cd=self.interval
        hero=self.tgtList[0]
        aim=hero
        distance=cal_dist(hero.pos,self.pos)
        for tgt in tgtList:
            _distance=cal_dist(tgt.pos,self.pos)
            if(_distance<distance):
                aim=tgt
                distance=_distance
        tpos=[self.pos[0],self.pos[1]]
        if(distance<=(self.atkrange)**2):
            bullet = CLS_Bullet(self.surface,self.pilot,self.bltrad,self.bltdur,tpos,1,self.bltspd,aim,self.bltatk+self.buffatk)
            bulletList.append(bullet)
        return
class CLS_Range_Building(CLS_Building):
    def __init__(self,screen,pos,side,player,bgcolor,prop,atk=5,polySideNum=-1,rad=10,hp=1000,atkrange=100,dur=1):
        super().__init__(screen,pos,side,player,polySideNum,rad,hp,atkrange,atk,0)
        self.bgcolor=bgcolor
        self.prop=prop# which property this attack is working on eg:"hp","speed+-","exp","atk+-"(...expandible)
        self.dur=dur
        return
    def action(self,ttList,bulletList):#hero: player/boss depend on which side this building is on
        self.cd-=1
        self.tgtList=ttList[1-self.side][0]+ttList[2][1-self.side]+ttList[3][1-self.side]# hero+troop+tower enemyList
        self.shoot(self.tgtList,bulletList)# attack enemy
        self.draw(ttList[0][0][0].fpos,ttList[0][0][0].pos)#self.totalList[0][0][0] is player
        return
    def shoot(self,tgtList,bulletList):
        if(self.cd>0):
            return
        self.cd=self.interval
        for tgt in tgtList:
            _distance=cal_dist(tgt.pos,self.pos)
            if(_distance<(self.atkrange)**2):
                if(self.prop=="hp-"):
                    tgt.hp-=self.atk
                elif(self.prop=="hp+"):
                    tgt.hp+=self.atk
                elif(self.prop=="exp"):
                    self.pilot.exp+=self.atk
                else:
                    #print(100,self.hp,tgt.hp)
                    tgt.buffList.append([self.prop,self.atk,self.dur,self])
                    #print("append:",[self.prop,self.atk,self.dur])
        return

STRATEGY_NUM=6 #five strategies from 0-5
stgNameList=["aggressive","passive atk","to_the_base","recall","stay","disperse"]
class CLS_Troop(CLS_item):
    def __init__(self,scr,pos,side,polySideNum=-1,strategy=0,rad=5,speedratio=1.5,hp=500,atkrange=50,atk=3,interval=15):
        #strategies 0 aggressive 1 passive 2 inagressive 3 passive calls 4 stay
        color=(255*side,0,255*(1-side))# color change according to side
        super().__init__(scr,rad,pos,[0,0],hp,color,atkrange+random.randint(-5,5),atk,interval++random.randint(-2,2),side,polySideNum)
        self.cd=interval
        self.tgtList=self#start with no target
        self.target=self
        self.spdratio=speedratio
        #self.totalList=ttList #DO I NEED IT? 
        self.strategy=strategy#0 for aggressive 1 for ingressive
        self.move=1
        self.speedflag=0
        self.bltdur=self.atkrange//self.bltspd*1.6
        return
    def action(self,ttList,bulletList):#hero: player/boss depend on which side this building is on
        self.move=1
        self.pilot=ttList[0][0][0] #FIXME(minor) only execute once | totalList[0][0][0] is player
        self.cd-=1
        self.check_buff()
        tgtpreList=ttList[1-self.side][0]+ttList[2][1-self.side]+ttList[3][1-self.side]# hero+troop+tower enemyList
        target = self.retarget(tgtpreList) # get target
        self.redirect(target)# get new speed
        self.shoot(self.target,bulletList)# attack enemy and stop(if possible)
        self.draw(self.pilot.fpos,self.pilot.pos)
        self.pos[0]+=self.speed[0]*self.move*(self.buffspeed+1)
        self.pos[1]+=self.speed[1]*self.move*(self.buffspeed+1)
        return
    def retarget(self,tgtList):
        base=tgtList[0]#FIXME IT should be first locate at enemy Base
        player=self.pilot
        self.target=base
        distance=cal_dist(base.pos,self.pos)
        if(self.strategy!=5):#running randomly
            self.speedflag=0
        else:
            self.speedflag+=1
            #print(self.speedflag)
        if(self.strategy!=2):#aggressive/passive target
            for tgt in tgtList:
                _distance=cal_dist(tgt.pos,self.pos)
                if(self.strategy==1 or self.strategy==3):# unless in shoot range, attack base(semi-aggressive/passive attacks)|moving to player,passive shooting
                    if(_distance<distance and _distance<(self.atkrange+self.rad+tgt.rad)**2):
                        self.target=tgt
                        distance=_distance
                elif(self.strategy==0 or self.strategy==4 or self.strategy==4):# in sight(larger) then shoot
                    if(_distance<distance and _distance<(self.sightrad)**2):
                        self.target=tgt
                        distance=_distance
        elif(self.strategy==2):#ingressive 
            self.target=base
            return base
        #moving direction
        if(self.strategy==4):# stay (bonus atkrange x1.2)(possibly get atk without power to fight back in a fix pos -> record the pos and free to move if see an enemy,go back to it when sees no enemy)
            return self
        elif(self.strategy==3):#running to player
            return player
        return self.target
    def redirect(self,tgt):# move to tgt
        if(self.strategy==5):#running randomly
            if(self.speedflag>=50):
                return
            self.speed = [self.spdratio*random.random()*(random.randint(0,1)-0.5)*2,self.spdratio*random.random()*(random.randint(0,1)-0.5)*2]
        else:
            self.speed = cal_speed(self.pos,tgt.pos,self.spdratio)
        return
    def shoot(self,tgt,bulletList):
        bonus=1
        distance=cal_dist(tgt.pos,self.pos)
        tpos=[self.pos[0],self.pos[1]]
        if(self.strategy==4 or self.move==0):
            bonus=1.2
        if(distance<=((self.atkrange+self.rad+tgt.rad)*bonus)**2):
            self.move=0
            if(self.cd>0):
                return
            self.cd=self.interval
            bullet = CLS_Bullet(self.surface,self.pilot,self.bltrad,self.bltdur,tpos,1,self.bltspd,tgt,self.bltatk+self.buffatk)
            bulletList.append(bullet)
        return
class CLS_GameAgent(object):
    def __init__(self,screen,player,Boss):
        self.pilot = player
        self.boss = Boss
        self.dotList=[]
        self.troopList=[[],[]] #self troop,opponent troop
        self.bulletList=[]
        self.towerList=[[],[]]
        self.surface=screen
        self.totalList=[[[self.pilot]],[[self.boss]],self.troopList,self.towerList]
        self.troopstrategy=0
    
    def draw_setting(self):#draw game map
        for dot in self.dotList:
            dot.draw(self.pilot.fpos,self.pilot.pos)
        self.draw_fence()
    def action(self):
        for item in self.troopList[0]+self.troopList[1]+self.towerList[0]+self.towerList[1]:
            dx,dy=dx,dy=cal_scrpos(item.pos,self.pilot.fpos,self.pilot.pos)
            item.draw_background(dx,dy)
        for troop in self.troopList[0]+self.troopList[1]:
            if(troop.side==0):
                troop.strategy=self.troopstrategy
            troop.action(self.totalList,self.bulletList)
            if(troop.hp<=0):
                self.troopList[troop.side].remove(troop)
        for tower in self.towerList[0]+self.towerList[1]:
            tower.action(self.totalList,self.bulletList)
            if(tower.hp<=0):
                self.towerList[tower.side].remove(tower)
        for bullet in self.bulletList:
            bullet.action()
            if(bullet.show==0):
                self.bulletList.remove(bullet)
        self.pilot.action()
        self.pilot_eat_dot_check()
        self.boss.action(self.totalList,self.bulletList)
        self.draw_setting()
    def pilot_eat_dot_check(self):
        for dot in self.dotList:
            dotpos = dot.pos
            dotplayerbound = (dot.rad + self.pilot.rad)**2
            distance = (dotpos[0]-self.pilot.pos[0])**2+(dotpos[1]-self.pilot.pos[1])**2
            if(distance < dotplayerbound):
                dot.rebirth()# rebirth dot
                self.pilot.exp += dot.pts
                self.pilot.hp += dot.pts//2
                self.displaytips("exp+",dot.pts)#FIXME a word box pop out to remind the player
        return
    def draw_fence(self):
        x,y = self.pilot.fpos[0]-self.pilot.pos[0],self.pilot.fpos[1]-self.pilot.pos[1]
        pygame.draw.rect(self.pilot.surface,FENCE_COLOR,(x,y,GRID_SIZE[0],GRID_SIZE[1]),2)
        return
    def create_dot(self):
        x=random.randint(0+DOT_R_RANGE[1],GRID_SIZE[0]-DOT_R_RANGE[1])
        y=random.randint(0+DOT_R_RANGE[1],GRID_SIZE[1]-DOT_R_RANGE[1])
        r=random.randint(DOT_R_RANGE[0],DOT_R_RANGE[1])
        color=(random.randint(50,150),random.randint(100,255),random.randint(100,255))
        dot = CLS_Dot(self.surface,[x,y],r,color)
        self.dotList.append(dot)
        return
    def displaytips(self,word,num):
        #show tips to remind the player
        return
    def build_item(self,itemtag,side,cost=0,dtype=0):#special tower should be build on CLS_Building and CLS_Troop(in another file perhaps?)
        self.pilot.exp-=cost
        if(itemtag=="shooter"):
            tpos=[self.pilot.pos[0],self.pilot.pos[1]]
            self.towerList[side].append(CLS_Building(self.surface,tpos,side,self.pilot,3))
        elif(itemtag=="gunner"):
            tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
            self.troopList[side].append(CLS_Troop(self.surface,tpos,side,0))
        elif(itemtag=="sniper"):
            tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
            self.troopList[side].append(CLS_Troop(self.surface,tpos,side,0,0,7,0.5,300,300,200,300))
        elif(itemtag=="factory"):#create troops every several hundreds frame(various kinds)
            pass
        elif(itemtag=="hptower"):#shoot atk<0 bullet(+HP) or have a range healing affect
            pass
        elif(itemtag=="slower"):#decrease speed within a big range
            if(dtype=="range"):
                tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
                self.troopList[side].append(CLS_Range_Building(self.surface,tpos,side,self.pilot,(30,50,0),"speed-",0.3,3,10,2000,300,2))
            elif(dtype=="blt"):#FIXME the side prob is not solved ,therfore unusable
                tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
                self.troopList[side].append(CLS_Building(self.surface,tpos,1-side,self.pilot,3,10,1000,200,-10,30))
            return
        elif(itemtag=="poisoner_T"):#with poison around it self,kill all who goes into it(atk should be very low)
            if(dtype=="range"):
                tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
                self.troopList[side].append(CLS_Range_Building(self.surface,tpos,side,self.pilot,(50,0,0),"hp-",0.5,-1,15,300))
            elif(dtype=="blt"):#FIXME the side prob is not solved ,therfore unusable
                tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
                self.troopList[side].append(CLS_Building(self.surface,tpos,1-side,self.pilot,3,10,1000,200,-10,30))
            return
        elif(itemtag=="poisoner_B"):#with poison around it self
            pass
        elif(itemtag=="bomber"):#AOE
            pass
        elif(itemtag=="range_killer_B"):#AOE
            pass
        elif(itemtag=="add_on_T"):#add on troops and buildings to give them buffs(or debuffs on enemy)
            pass
        elif(itemtag=="rand_add_on"):#random(buff/debuff) very low cost
            pass
        elif(itemtag=="suiside_team"):#high speed small range suiside troop_team(3 in a roll)
            pass
        elif(itemtag=="exp_gainer"):#gives you a constant way to increase Exp
            pass
        elif(itemtag=="map_destroyer"):# with unlimited bullet range and bullet dur(long interval)
            pass
        elif(itemtag=="mine"):#explosive(building,that are in special mineList/fake_pos)
            pass
        elif(itemtag=="portal"):#experimental player-use one-way(2ways also ok) portal(at most one pair on map first click drops ins second drops outs) 
            pass
        elif(itemtag=="dummy"):# a robot without atk but can attract fire(HP++)
            pass
        elif(itemtag=="healer"):#shoot bullet to heal other troop-members(player excluded)
            pass
        elif(itemtag=="line-atk_T"):#draw lines between tower and enemy,cause an increasing atk at each one troop
            pass
        elif(itemtag=="alert_tower"):#contains a certain amount of troops,release all when detect enemy
            pass
        elif(itemtag=="patrol_team"):#several troops patrolling on a line (two clicks to place)
            pass
        elif(itemtag=="chaos_tower"):#make player's motion randomize
            pass
        else:
            print("building command not found")
            self.pilot.exp+=cost
        return

    

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

