import pygame, math
from global_variables import *
from calc import *
import sys


class Renderer:
    def __init__(self, surface):
        self.surface = surface

    # fence
    def draw_fence(self, color, x, y):
        pygame.draw.rect(self.surface, color, (x, y, GRID_SIZE[0], GRID_SIZE[1]), 2)

    # minimap
    def draw_minimap_background(self, x_start_location, x_len, y_len):
        pygame.draw.rect(
            self.surface,
            (255, 255, 255),
            (x_start_location - 3, 0, x_len + 2, y_len + 2),
        )
        pygame.draw.rect(
            self.surface, (0, 0, 0), (x_start_location - 2, 1, x_len, y_len)
        )

    def draw_minymap_elements(self, color, x, y, radius):
        pygame.draw.circle(self.surface, color, (x, y), radius)

    # dot
    def draw_dot(self, pos, color, rad, fpos, ppos):
        # use player Position(ppos) to draw self
        dx, dy = pos[0] - ppos[0] + fpos[0], pos[1] - ppos[1] + fpos[1]
        if dx + rad < 0 or dx - rad > SCREEN_W or dy + rad < 0 or dy - rad > SCREEN_H:
            return
        pygame.draw.circle(self.surface, color, [dx, dy], rad, 0)
        return

    # cls_main
    def draw_cls(self, cls, fpos, ppos, tag=0):  # use player Position to draw self
        if tag == 1:
            print("draw")
        dx, dy = cal_scrpos(cls.pos, fpos, ppos)
        if (
            dx + cls.rad < 0
            or dx - cls.rad > SCREEN_W
            or dy + cls.rad < 0
            or dy - cls.rad > SCREEN_H
        ):
            if tag == 1:
                print("out of range")
            return -1
        if tag == 0:
            pygame.draw.circle(self.surface, cls.color, [dx, dy], cls.rad, 0)
            self.draw_cls_extras(cls, dx, dy, cls.poly)
        elif tag == 2:
            if dx < 0 or dx > SCREEN_W or dy < 0 or dy > SCREEN_H:
                return -1
            return (dx - cls.rad, dy + cls.rad)
        if tag == 1:
            print("success", cls.color, dx, dy)
        return

    def draw_cls_extras(self, cls, x, y, sideNum):
        pointList = []
        r = cls.rad / 2
        if sideNum == 0:
            pygame.draw.circle(self.surface, cls.dcolor, [x, y], r, 0)
            return
        if sideNum == -1:
            return
        for i in range(sideNum):
            ang = 2 * math.pi / sideNum * i
            pointList.append((x + r * math.cos(ang), y + r * math.sin(ang)))
        pygame.draw.polygon(self.surface, cls.dcolor, pointList, 0)
        return

    def draw_cls_background(self, cls, x, y):
        pygame.draw.circle(self.surface, cls.bgcolor, [x, y], cls.atkrange, 0)

    # cls_player
    def draw_player(self, player):
        pygame.draw.circle(self.surface, player.color, player.fpos, player.rad, 0)
        pygame.draw.rect(self.surface, player.rectcolor, player.rect, 2)

    # draw text
    def draw_text(self, player, agent):
        fontScore = pygame.font.Font(None, 28)
        img_text = fontScore.render(
            "exp:" + str(agent.pilot.exp), True, (250, 250, 250)
        )
        self.surface.blit(img_text, (10, 10))
        img_text = fontScore.render(
            "strategy:" + str(stgNameList[agent.troopstrategy]), True, (250, 250, 250)
        )
        self.surface.blit(img_text, (10, 30))
        img_text = fontScore.render(
            "HP:" + str(agent.pilot.hp) + "/" + str(hpList[agent.pilot.lv]),
            True,
            (250, 250, 250),
        )
        self.surface.blit(img_text, (10, 50))
        for item in (
            agent.towerList[0]
            + agent.towerList[1]
            + agent.troopList[0]
            + agent.troopList[1]
        ):
            scrpos = item.draw(player.fpos, player.pos, 2)
            if scrpos == -1:
                continue
            img_text = fontScore.render("HP:" + str(item.hp), True, (250, 250, 250))
            self.surface.blit(img_text, scrpos)
        scrpos = agent.boss.draw(player.fpos, player.pos, 2)
        if scrpos != -1:
            img_text = fontScore.render(
                "HP:" + str(agent.boss.hp), True, (250, 250, 250)
            )
            self.surface.blit(img_text, scrpos)
