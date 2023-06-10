from .object import Object

class Bullet(Object):
    def __init__(self, map_bounds, x, y, v) -> None:
        super().__init__(map_bounds,x,y,10)
        self.color = (255,0,0)
        self.velocity = v

        
    def update_position(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def move(self):
        self.update_position()
        

        

    
    

        