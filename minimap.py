from global_variables import SCREEN_W, SCREEN_H, GRID_SIZE
from renderer import Renderer

"""
2023/1/25
the minimap class is used inside the cls game agent
you can draw the minimap at the right top
@Ling
"""
"""
2023/1/26
I found a bug that the opponent troops and towers are displayed wrongly in the minimap?
BUG @Ling
"""


class MiniMap:
    def __init__(self, gameAgent, renderer=Renderer(None)):
        self.gameAgent = gameAgent
        self.dotList = []
        self.troopList = [[], []]
        self.towerList = [[], []]
        self.playerLoc = []
        self.renderer = renderer

        self.y_len = int(SCREEN_H / 5)
        self.y_g_len = SCREEN_H
        self.x_len = int(self.y_len / GRID_SIZE[1] * GRID_SIZE[0])
        self.x_g_len = int(self.y_g_len / GRID_SIZE[1] * GRID_SIZE[0])
        self.r = GRID_SIZE[1] / self.y_len
        self.g_r = GRID_SIZE[1] / self.y_g_len
        # this makes no difference in 2500x2500

    def sync(self):
        self.dotList = self.gameAgent.dotList
        self.troopList = self.gameAgent.troopList
        self.towerList = self.gameAgent.towerList
        self.playerLoc = self.gameAgent.pilot.pos

    def draw_background(self):
        # the difference of a pixel is unnoticable
        x_start_location = SCREEN_W - self.x_len
        x_len = self.x_len
        y_len = self.y_len
        self.renderer.draw_minimap_background(x_start_location, x_len, y_len)

    def draw(self, x, y, radius, color):
        """
        x= real x
        y= real y
        color=(r,g,b)
        """
        fx = SCREEN_W - self.x_len + int(x / self.r)
        fy = int(y / self.r)
        self.renderer.draw_minimap_elements(color, fx, fy, radius)

        # print(fx,fy)

    def draw_main(self):
        self.draw_background()
        for dot in self.dotList:
            self.draw(dot.pos[0], dot.pos[1], 1, (100, 100, 100))
        self.draw(self.playerLoc[0], self.playerLoc[1], 3, (0, 0, 255))
        # self in blue, enemy in red
        for troop in self.troopList[0]:
            self.draw(troop.pos[0], troop.pos[1], 1, (100, 100, 255))
        for troop in self.towerList[1]:
            self.draw(troop.pos[0], troop.pos[1], 1, (255, 100, 0))
        for tower in self.towerList[0]:
            self.draw(tower.pos[0], tower.pos[1], 2, (100, 100, 255))
        for tower in self.troopList[1]:
            self.draw(tower.pos[0], tower.pos[1], 2, (255, 100, 0))


"""
press m to display giantmap
"""


class GiantMap(MiniMap):
    def draw_background(self):
        x_start_location = (SCREEN_W - self.x_g_len) / 2
        x_len = self.x_g_len
        y_len = self.y_g_len
        self.renderer.draw_minimap_background(x_start_location, x_len, y_len)
        # pygame.draw.rect(self.surface,(255,255,255),((SCREEN_W-self.x_g_len)/2-3,0,self.x_g_len+2,self.y_g_len+2))
        # pygame.draw.rect(self.surface,(0,0,0),((SCREEN_W-self.x_g_len)/2-2,1,self.x_g_len,self.y_g_len))

    def draw(self, x, y, radius, color):
        radius = radius * self.r / self.g_r
        fx = (SCREEN_W - self.x_g_len) / 2 + int(x / self.g_r)
        fy = int(y / self.g_r)
        self.renderer.draw_minimap_elements(color, fx, fy, radius)
