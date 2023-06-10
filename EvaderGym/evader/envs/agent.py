from .object import Object
import math

class Agent(Object):
    def __init__(self, map_bounds) -> None:
        self.bounds_x = (map_bounds[0], map_bounds[2])
        self.bounds_y = (map_bounds[1], map_bounds[3])

        super().__init__(map_bounds)
        
        self.x = self.draw_loc_x()
        self.y = self.draw_loc_y()
        self.color = (0,255,0)

        self.r = 15
        self.speed = 5
        # 3 2 1
        # 4 8 0
        # 5 6 7
        pi4 = math.pi / 4
        self.actions = {
            0: [self.speed * math.cos(pi4 * 0), self.speed * math.sin(pi4 * 0)],
            1: [self.speed * math.cos(pi4 * 1), self.speed * math.sin(pi4 * 1)],
            2: [self.speed * math.cos(pi4 * 2), self.speed * math.sin(pi4 * 2)],
            3: [self.speed * math.cos(pi4 * 3), self.speed * math.sin(pi4 * 3)],
            4: [self.speed * math.cos(pi4 * 4), self.speed * math.sin(pi4 * 4)],
            5: [self.speed * math.cos(pi4 * 5), self.speed * math.sin(pi4 * 5)],
            6: [self.speed * math.cos(pi4 * 6), self.speed * math.sin(pi4 * 6)],
            7: [self.speed * math.cos(pi4 * 7), self.speed * math.sin(pi4 * 7)],
            8: [0,0]
        }

    def move(self, action=8):
        v = self.actions[action]
        self.x += v[0]
        self.y += v[1]
        if(not self.check_bounds()):
            self.x -= v[0]
            self.y -= v[1]
        pass