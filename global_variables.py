# globals
SCREEN_W, SCREEN_H = 1000, 600
SCREEN_SIZE = [SCREEN_H, SCREEN_W]
GRID_SIZE = [2500, 2500]
FENCE_COLOR = (150, 150, 200)
DOT_R_RANGE = [5, 15]  # the range of the dot's radius


# needed to plan for more upgrades
radList = [-1, 10, 20, 30, 40, 50]  # radius of different levels
spdList = [-1, 3, 2.75, 2.5, 2.25, 2]  # speed of different levels
expList = [
    -1,
    300,
    500,
    1000,
    2000,
    1000000,
]  # exp needed for different levels | <300 lv1 || 300-500 lv2 || 500-1000 lv3 |
colorList = [
    -1,
    (255, 255, 255),
    (255, 200, 200),
    (255, 150, 150),
    (255, 100, 100),
    (255, 70, 70),
]
atkList = [
    [-1, -1, -1, -1],
    [20, 8, 200, 3],
    [40, 9, 250, 4],
    [60, 10, 300, 5],
    [80, 15, 400, 6],
    [100, 20, 600, 7],
]  # [atk,rad,dur,spd]
hpList = [-10000, 1000, 1500, 2000, 3000, 10000]

STRATEGY_NUM = 6  # five strategies from 0-5
stgNameList = ["aggressive", "passive atk", "to_the_base", "recall", "stay", "disperse"]

expConsumption = [2, 100, 300, 500]
