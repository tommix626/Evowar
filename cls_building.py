from cls_main import CLS_item
from cls_bullet import CLS_Bullet
from calc import cal_dist


class CLS_Building(CLS_item):
    def __init__(
        self,
        renderer,
        pos,
        side,
        player,
        polySideNum=-1,
        rad=10,
        hp=1000,
        atkrange=200,
        atk=10,
        interval=30,
    ):
        color = (255 * side, 0, 255 * (1 - side))  # color change according to side
        super().__init__(
            renderer,
            rad,
            pos,
            [0, 0],
            hp,
            color,
            atkrange,
            atk,
            interval,
            side,
            polySideNum,
        )
        self.cd = interval  # cd decrease and reset with time; interval is a constant
        self.pilot = player
        self.bltdur = self.atkrange // self.bltspd * 1.1
        return

    def action(
        self, ttList, bulletList
    ):  # hero: player/boss depend on which side this building is on
        self.cd -= 1
        self.check_buff()
        self.tgtList = (
            ttList[1 - self.side][0]
            + ttList[2][1 - self.side]
            + ttList[3][1 - self.side]
        )  # hero+troop+tower enemyList
        self.shoot(self.tgtList, bulletList)  # attack enemy
        self.draw(
            ttList[0][0][0].fpos, ttList[0][0][0].pos
        )  # self.totalList[0][0][0] is player
        return

    def shoot(self, tgtList, bulletList):
        if self.cd > 0:
            return
        self.cd = self.interval
        hero = self.tgtList[0]
        aim = hero
        distance = cal_dist(hero.pos, self.pos)
        for tgt in tgtList:
            _distance = cal_dist(tgt.pos, self.pos)
            if _distance < distance:
                aim = tgt
                distance = _distance
        tpos = [self.pos[0], self.pos[1]]
        if distance <= (self.atkrange) ** 2:
            bullet = CLS_Bullet(
                self.renderer,
                self.pilot,
                self.bltrad,
                self.bltdur,
                tpos,
                1,
                self.bltspd,
                aim,
                self.bltatk + self.buffatk,
            )
            bulletList.append(bullet)
        return


class CLS_Range_Building(CLS_Building):
    def __init__(
        self,
        renderer,
        pos,
        side,
        player,
        bgcolor,
        prop,
        atk=5,
        polySideNum=-1,
        rad=10,
        hp=1000,
        atkrange=100,
        dur=1,
    ):
        super().__init__(
            renderer, pos, side, player, polySideNum, rad, hp, atkrange, atk, 0
        )
        self.bgcolor = bgcolor
        self.prop = prop  # which property this attack is working on eg:"hp","speed+-","exp","atk+-"(...expandible)
        self.dur = dur
        return

    def action(
        self, ttList, bulletList
    ):  # hero: player/boss depend on which side this building is on
        self.cd -= 1
        self.tgtList = (
            ttList[1 - self.side][0]
            + ttList[2][1 - self.side]
            + ttList[3][1 - self.side]
        )  # hero+troop+tower enemyList
        self.shoot(self.tgtList, bulletList)  # attack enemy
        self.draw(
            ttList[0][0][0].fpos, ttList[0][0][0].pos
        )  # self.totalList[0][0][0] is player
        return

    def shoot(self, tgtList, bulletList):
        if self.cd > 0:
            return
        self.cd = self.interval
        for tgt in tgtList:
            _distance = cal_dist(tgt.pos, self.pos)
            if _distance < (self.atkrange) ** 2:
                if self.prop == "hp-":
                    tgt.hp -= self.atk
                elif self.prop == "hp+":
                    tgt.hp += self.atk
                elif self.prop == "exp":
                    self.pilot.exp += self.atk
                else:
                    # print(100,self.hp,tgt.hp)
                    tgt.buffList.append([self.prop, self.atk, self.dur, self])
                    # print("append:",[self.prop,self.atk,self.dur])
        return
