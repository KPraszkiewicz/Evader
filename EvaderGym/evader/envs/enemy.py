import random
import math
from .object import Object
from .bullet import Bullet

class Enemy(Object):
    def __init__(self, map_bounds, type) -> None:
        super().__init__(map_bounds)
        
        self.x = self.draw_loc_x()
        self.y = self.draw_loc_y()
        self.color = (0,0,255)

        self.r = 15
        self.speed = 5
        self.bullet_speed = 10
        self.shoot_frequency = 10

        self.type = type
        self.gen_new_dest()
        self.shoot_wait = 0
        

    # (min_x, min_y, max_x, max_y)
    def gen_new_dest(self):
        self.dest = [self.draw_loc_x(), self.draw_loc_y()]
        self.v = self.calc_velocity([self.x,self.y],self.dest,self.speed)


    
    
    def shoot(self, target=[0,0]):
        self.shoot_wait = 0
        if self.type == '.':
            vector = self.calc_velocity([self.x, self.y],target, self.bullet_speed)
            return [
                Bullet(self.map_bounds, self.x, self.y, vector)
            ]
        
        elif self.type == 'x':
            y = self.bullet_speed * math.sin(math.pi / 4)
            x = self.bullet_speed * math.cos(math.pi / 4)
            return [
                Bullet(self.map_bounds, self.x, self.y, (x,y)),
                Bullet(self.map_bounds, self.x, self.y, (-x,y)),
                Bullet(self.map_bounds, self.x, self.y, (x,-y)),
                Bullet(self.map_bounds, self.x, self.y, (-x,-y)),
            ]

        elif self.type == '+':
            y = self.bullet_speed
            x = self.bullet_speed
            return [
                Bullet(self.map_bounds, self.x, self.y, (x,0)),
                Bullet(self.map_bounds, self.x, self.y, (-x,0)),
                Bullet(self.map_bounds, self.x, self.y, (0,y)),
                Bullet(self.map_bounds, self.x, self.y, (0,-y)),
            ]
        
    def move(self):

        while self.calc_distance_to(self.dest) < self.speed:
            self.gen_new_dest()

        self.shoot_wait += 1

        self.x += self.v[0]
        self.y += self.v[1]

        pass