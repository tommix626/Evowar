import random
from global_variables import DOT_R_RANGE, GRID_SIZE


class Dot(object):
    def __init__(self, renderer, pos, rad, color=(200, 200, 200)):
        self.rad = rad
        self.color = color
        self.pos = pos  # real position on the grid
        self.renderer = renderer
        self.pts = self.rad * 2

    def draw(self, fpos, ppos):  # use player Position(ppos) to draw self
        self.renderer.draw_dot(self.pos, self.color, self.rad, fpos, ppos)

    def rebirth(self):
        self.pos[0] = random.randint(0 + DOT_R_RANGE[1], GRID_SIZE[0] - DOT_R_RANGE[1])
        self.pos[1] = random.randint(0 + DOT_R_RANGE[1], GRID_SIZE[1] - DOT_R_RANGE[1])
        self.rad = random.randint(DOT_R_RANGE[0], DOT_R_RANGE[1])
        self.pts = self.rad * 2
        self.color = (
            random.randint(50, 150),
            random.randint(100, 255),
            random.randint(100, 255),
        )
