import pygame
import math
import random

class Object():
    def __init__(self, map_bounds, x = 0, y = 0, r = 10, color=(0,0,0)) -> None:
        self.x = x
        self.y = y

        self.r = r
        self.map_bounds = map_bounds
        self.bounds_x = (map_bounds[0], map_bounds[2])
        self.bounds_y = (map_bounds[1], map_bounds[3])

        self.color = color
        
    def draw(self,canvas):
        pygame.draw.circle(
            canvas,
            self.color,
            [self.x,self.y],
            self.r,
        )

    def draw_loc_x(self):
        return random.randint(self.bounds_x[0] + self.r, self.bounds_x[1] - self.r)
    
    def draw_loc_y(self):
        return random.randint(self.bounds_y[0] + self.r, self.bounds_y[1] - self.r)
    
    def calc_velocity(self, src, dest, l):
        vector = [dest[0] - src[0], dest[1] - src[1]]
        length = math.sqrt(vector[0]**2 + vector[1]**2)
        vector[0] = vector[0] / length * l
        vector[1] = vector[1] / length * l
        return vector
    
    def calc_distance(self, a, b):
        vector = [a[0] - b[0], a[1] - b[1]]
        return math.sqrt(vector[0]**2 + vector[1]**2)

    def calc_distance_to(self, b):
        vector = [self.x - b[0], self.y - b[1]]
        return math.sqrt(vector[0]**2 + vector[1]**2)

    # true if x,y in bounds
    def check_bounds(self):
        if(self.bounds_x[0] > self.x - self.r):
            return False
        if(self.bounds_x[1] < self.x + self.r):
            return False
        if(self.bounds_y[0] > self.y - self.r):
            return False
        if(self.bounds_y[1] < self.y + self.r):
            return False
        return True

    def check_collision(self, obj):
        vector = [self.x - obj.x, self.y - obj.y]
        length = math.sqrt(vector[0]**2 + vector[1]**2)
        r = self.r + obj.r
        if(length < r):
            return True
        return False