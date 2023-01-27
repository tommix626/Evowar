import random, pygame
from cls_main import CLS_item
from cls_bullet import CLS_Bullet
from calc import cal_dist, cal_scrpos, cal_speed


class CLS_Troop(CLS_item):
    def __init__(
        self,
        renderer,
        pos,
        side,
        polySideNum=-1,
        strategy=0,
        rad=5,
        speedratio=1.5,
        hp=500,
        atkrange=50,
        atk=3,
        interval=15,
    ):
        # strategies 0 aggressive 1 passive 2 inagressive 3 passive calls 4 stay
        color = (255 * side, 0, 255 * (1 - side))  # color change according to side
        super().__init__(
            renderer,
            rad,
            pos,
            [0, 0],
            hp,
            color,
            atkrange + random.randint(-5, 5),
            atk,
            interval + +random.randint(-2, 2),
            side,
            polySideNum,
        )
        self.cd = interval
        self.tgtList = self  # start with no target
        self.target = self
        self.spdratio = speedratio
        # self.totalList=ttList #DO I NEED IT?
        self.strategy = strategy  # 0 for aggressive 1 for ingressive
        self.move = 1
        self.speedflag = 0
        self.bltdur = self.atkrange // self.bltspd * 1.6
        return

    def action(
        self, ttList, bulletList
    ):  # hero: player/boss depend on which side this building is on
        self.move = 1
        self.pilot = ttList[0][0][
            0
        ]  # FIXME(minor) only execute once | totalList[0][0][0] is player
        self.cd -= 1
        self.check_buff()
        tgtpreList = (
            ttList[1 - self.side][0]
            + ttList[2][1 - self.side]
            + ttList[3][1 - self.side]
        )  # hero+troop+tower enemyList
        target = self.retarget(tgtpreList)  # get target
        self.redirect(target)  # get new speed
        self.shoot(self.target, bulletList)  # attack enemy and stop(if possible)
        self.draw(self.pilot.fpos, self.pilot.pos)
        self.pos[0] += self.speed[0] * self.move * (self.buffspeed + 1)
        self.pos[1] += self.speed[1] * self.move * (self.buffspeed + 1)
        return

    def retarget(self, tgtList):
        base = tgtList[0]  # FIXME IT should be first locate at enemy Base
        player = self.pilot
        self.target = base
        distance = cal_dist(base.pos, self.pos)
        if self.strategy != 5:  # running randomly
            self.speedflag = 0
        else:
            self.speedflag += 1
            # print(self.speedflag)
        if self.strategy != 2:  # aggressive/passive target
            for tgt in tgtList:
                _distance = cal_dist(tgt.pos, self.pos)
                if (
                    self.strategy == 1 or self.strategy == 3
                ):  # unless in shoot range, attack base(semi-aggressive/passive attacks)|moving to player,passive shooting
                    if (
                        _distance < distance
                        and _distance < (self.atkrange + self.rad + tgt.rad) ** 2
                    ):
                        self.target = tgt
                        distance = _distance
                elif (
                    self.strategy == 0 or self.strategy == 4 or self.strategy == 4
                ):  # in sight(larger) then shoot
                    if _distance < distance and _distance < (self.sightrad) ** 2:
                        self.target = tgt
                        distance = _distance
        elif self.strategy == 2:  # ingressive
            self.target = base
            return base
        # moving direction
        if (
            self.strategy == 4
        ):  # stay (bonus atkrange x1.2)(possibly get atk without power to fight back in a fix pos -> record the pos and free to move if see an enemy,go back to it when sees no enemy)
            return self
        elif self.strategy == 3:  # running to player
            return player
        return self.target

    def redirect(self, tgt):  # move to tgt
        if self.strategy == 5:  # running randomly
            if self.speedflag >= 50:
                return
            self.speed = [
                self.spdratio * random.random() * (random.randint(0, 1) - 0.5) * 2,
                self.spdratio * random.random() * (random.randint(0, 1) - 0.5) * 2,
            ]
        else:
            self.speed = cal_speed(self.pos, tgt.pos, self.spdratio)
        return

    def shoot(self, tgt, bulletList):
        bonus = 1
        distance = cal_dist(tgt.pos, self.pos)
        tpos = [self.pos[0], self.pos[1]]
        if self.strategy == 4 or self.move == 0:
            bonus = 1.2
        if distance <= ((self.atkrange + self.rad + tgt.rad) * bonus) ** 2:
            self.move = 0
            if self.cd > 0:
                return
            self.cd = self.interval
            bullet = CLS_Bullet(
                self.renderer,
                self.pilot,
                self.bltrad,
                self.bltdur,
                tpos,
                1,
                self.bltspd,
                tgt,
                self.bltatk + self.buffatk,
            )
            bulletList.append(bullet)
        return
