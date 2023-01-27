from cls_main import CLS_item
from calc import cal_dist, cal_scrpos, cal_speed


class CLS_Bullet(CLS_item):
    def __init__(
        self,
        renderer,
        player,
        rad,
        duration,
        pos,
        flag,
        spd,
        tgt,
        atk,
        totalList=0,
        selfidx=-1,
    ):  # for linear: spd is a tuple tgt=0,need totalList,selfidx is index of self in totalList that should not be a target
        self.rad = rad
        self.duration = duration
        self.mode = flag
        self.pos = pos
        self.atk = atk
        self.pilot = player  # use for draw self
        self.renderer = renderer
        self.color = (0, 255, 0)
        self.poly = -1
        self.bgcolor = None
        if flag:
            self.target = tgt
            self.spdratio = spd
            self.redirect()
        else:
            self.speed = spd
            self.idx = selfidx
            self.targetList = totalList
        self.show = 1
        return

    def action(self):
        if self.show == 0:
            return
        self.duration -= 1
        if self.duration < 0:
            self.show = 0
            return
        self.bulletmove()
        self.draw(self.pilot.fpos, self.pilot.pos, 0)
        return

    def bulletmove(self):
        if self.mode:  # target at one
            self.redirect()
            if cal_dist(self.pos, self.target.pos) <= (self.rad + self.target.rad) ** 2:
                self.target.hp -= self.atk
                self.show = 0
        else:  # taarget for all
            for i in range(len(self.targetList)):
                if i == self.idx:
                    continue
                for j in range(len(self.targetList[i])):
                    for target in self.targetList[i][j]:
                        if (
                            cal_dist(self.pos, target.pos)
                            < (self.rad + target.rad) ** 2
                        ):
                            target.hp -= self.atk // 5
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        return

    def redirect(self):
        self.speed = cal_speed(self.pos, self.target.pos, self.spdratio)
        return
