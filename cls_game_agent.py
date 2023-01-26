import pygame,random
from calc import cal_dist,cal_scrpos,cal_speed
from global_variables import FENCE_COLOR,GRID_SIZE,DOT_R_RANGE,expList,expConsumption
from cls_troop import CLS_Troop
from cls_building import CLS_Building,CLS_Range_Building
from cls_dot import CLS_Dot
from minimap import MinyMap,GiantMap
from renderer import Renderer
class CLS_GameAgent(object):
    def __init__(self,renderer,player,Boss):
        self.pilot = player
        self.boss = Boss
        self.dotList=[]
        self.troopList=[[],[]] #self troop,opponent troop
        self.bulletList=[]
        self.towerList=[[],[]]
        #self.surface=screen
        self.totalList=[[[self.pilot]],[[self.boss]],self.troopList,self.towerList]
        self.troopstrategy=0
        self.renderer=renderer
        self.minyMap=MinyMap(self,self.renderer)
        self.giantMap=GiantMap(self,self.renderer)
        self.mapFlag=-1
    
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
        #minymap section, after most calculations
        self.minyMap.sync()
        self.giantMap.sync()
        self.minyMap.draw_main()
        if self.mapFlag==1:
            self.giantMap.draw_main()
        
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
        self.renderer.draw_fence(FENCE_COLOR,x,y)
        return
    def create_dot(self):
        x=random.randint(0+DOT_R_RANGE[1],GRID_SIZE[0]-DOT_R_RANGE[1])
        y=random.randint(0+DOT_R_RANGE[1],GRID_SIZE[1]-DOT_R_RANGE[1])
        r=random.randint(DOT_R_RANGE[0],DOT_R_RANGE[1])
        color=(random.randint(50,150),random.randint(100,255),random.randint(100,255))
        dot = CLS_Dot(self.renderer,[x,y],r,color)
        self.dotList.append(dot)
        return

    def display_map(self):
        #1 stands for openmap -1 stands for a closed map
        self.mapFlag=self.mapFlag*(-1)

    def displaytips(self,word,num):
        #show tips to remind the player
        return
    def build_item(self,itemtag,side,cost=0,dtype=0):#special tower should be build on CLS_Building and CLS_Troop(in another file perhaps?)
        self.pilot.exp-=cost
        if(itemtag=="shooter"):
            tpos=[self.pilot.pos[0],self.pilot.pos[1]]
            #here
            #self.pilot.exp=self.pilot.exp-expConsumption[3]
            self.towerList[side].append(CLS_Building(self.renderer,tpos,side,self.pilot,3))
        elif(itemtag=="gunner"):
            tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
            self.troopList[side].append(CLS_Troop(self.renderer,tpos,side,0))
        elif(itemtag=="sniper"):
            tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
            self.troopList[side].append(CLS_Troop(self.renderer,tpos,side,0,0,7,0.5,300,300,200,300))
        elif(itemtag=="factory"):#create troops every several hundreds frame(various kinds)
            pass
        elif(itemtag=="hptower"):#shoot atk<0 bullet(+HP) or have a range healing affect
            pass
        elif(itemtag=="slower"):#decrease speed within a big range
            self.pilot.exp=self.pilot.exp-expConsumption[2]
            if(dtype=="range"):
                tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
                self.troopList[side].append(CLS_Range_Building(self.renderer,tpos,side,self.pilot,(30,50,0),"speed-",0.3,3,10,2000,300,2))
            elif(dtype=="blt"):#FIXME the side prob is not solved ,therfore unusable
                tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
                self.troopList[side].append(CLS_Building(self.renderer,tpos,1-side,self.pilot,3,10,1000,200,-10,30))
            return
        elif(itemtag=="poisoner_T"):#with poison around it self,kill all who goes into it(atk should be very low)
            self.pilot.exp=self.pilot.exp-expConsumption[2]
            if(dtype=="range"):
                tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
                self.troopList[side].append(CLS_Range_Building(self.renderer,tpos,side,self.pilot,(50,0,0),"hp-",0.5,-1,15,300))
            elif(dtype=="blt"):#FIXME the side prob is not solved ,therfore unusable
                tpos=[self.pilot.pos[0]+random.randint(-20,20),self.pilot.pos[1]+random.randint(-20,20)]
                self.troopList[side].append(CLS_Building(self.renderer,tpos,1-side,self.pilot,3,10,1000,200,-10,30))
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