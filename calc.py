def cal_dist(pos1, pos2):  # calulate the distance between two point
    distance = (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2
    return distance


def cal_speed(
    pos1, pos2, ratio
):  # calculate the needed x-y speed (pos1 --> pos2) satisfy speedx^2+speedy^2=ratio^2 |speed|=ratio
    dr = (cal_dist(pos1, pos2)) ** (1 / 2) + 0.001
    dx, dy = pos2[0] - pos1[0], pos2[1] - pos1[1]
    speed = [dx * ratio / dr // 0.001 / 1000, dy * ratio / dr // 0.001 / 1000]
    return speed


def cal_scrpos(pos, fpos, ppos):
    return pos[0] - ppos[0] + fpos[0], pos[1] - ppos[1] + fpos[1]
