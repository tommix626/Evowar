from global_variables import SCREEN_SIZE
from renderer import Renderer

BULLET_RAD_INIT, BULLET_DUR_INIT, BULLET_ATK_INIT, BULLET_SPD_INIT = 3, 80, 50, 3
SIGHT_RAD_INIT = min(SCREEN_SIZE) // 2.2
"""
2023/1/26
It is to note that I have already changed screen to renderer. The drawing functions still work, but I still suggest using
the one in renderer
@Ling
"""


class item(object):
    def __init__(
        self,
        renderer,
        rad,
        pos,
        speed,
        hp,
        color,
        atkrange,
        atk,
        interval,
        side,
        polySideNum,
    ):
        self.rad = rad
        self.pos = pos
        self.speed = speed
        self.hp = hp
        # this should be deleted after a full transfer to renderer
        # self.surface=screen
        self.color = color
        self.dcolor = (255 - color[0], 255 - color[1], 255 - color[2])
        self.atkrange = atkrange
        self.atk = atk
        self.interval = interval
        self.side = side
        self.bltrad = BULLET_RAD_INIT
        self.bltdur = BULLET_DUR_INIT
        self.bltatk = atk
        self.bltspd = BULLET_SPD_INIT
        self.sightrad = SIGHT_RAD_INIT
        self.poly = polySideNum
        self.buffList = (
            []
        )  # for rebuffing contain inverse-buff affect and time to release |("atk",3,20,BuildingX)->BuildingX give this item a +3atk buff lasting 20 frame |
        self.buffatk, self.buffspeed = 0, 0
        self.bgcolor = None
        """
        if renderer==None:
           self.renderer=Renderer(screen)
        else:
            self.renderer=renderer
        return
        """
        self.renderer = renderer

    def draw(self, fpos, ppos, tag=0):
        # moved to renderer
        return self.renderer.draw_cls(self, fpos, ppos, tag)

    def draw_extras(self, x, y, sideNum=0):
        # moved to renderer
        # FIXME can be reload to mark different buildings (will consider to use it to distinct between enemy and self)
        self.renderer.draw_extras(self, x, y, sideNum)

    def draw_background(self, dx, dy):  # for special towers
        if self.bgcolor is None:
            return
        self.renderer.draw_background(self, dx, dy)
        return

    def check_buff(self):
        self.buffatk, self.buffspeed = 0, 0
        # one building can only cause one buff of a kind
        for i in range(len(self.buffList) - 1):
            for j in range(i + 1, len(self.buffList)):
                if (
                    self.buffList[i][3] == self.buffList[j][3]
                    and self.buffList[i][0] == self.buffList[j][0]
                ):
                    self.buffList[i][2] = -1
        for buff in self.buffList:
            print(buff[2])
            if buff[2] <= 0:
                continue
            buff[2] -= 1
            if buff[0] == "atk+":
                self.buffatk += buff[1]
            elif buff[0] == "atk-":
                self.buffatk -= buff[1]
            elif buff[0] == "speed-":
                self.buffspeed -= buff[1]
            elif buff[0] == "speed+":
                self.buffspeed += buff[1]
        for buff in self.buffList:
            print(buff[2])
            if buff[2] <= 0:
                self.buffList.remove(buff)
                continue
            buff[2] -= 1
        # print("buff:",self.buffatk,self.buffspeed)
