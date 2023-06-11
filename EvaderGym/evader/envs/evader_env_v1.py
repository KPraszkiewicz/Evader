import numpy as np 
import matplotlib.pyplot as plt
import PIL.Image as Image
import gymnasium
import random
import pygame
from gymnasium import Env, spaces
import time

from .agent import Agent
from .bullet import Bullet
from .enemy import Enemy

class EvaderEnv_v1(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, **kwargs) -> None:
        super().__init__()

        # dimensions of the grid
        self.width = kwargs.get('width',600)
        self.height = kwargs.get('height',600)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        map_bounds = (0,0,self.width,self.height)
        self.map_bounds = map_bounds

        self.enemies = [Enemy(map_bounds,'x'),Enemy(map_bounds,'+'),Enemy(map_bounds,'.')]
        self.agents = [Agent(map_bounds)]
        self.bullets = []

        self.window_size = (self.width,self.height)
        self.observation_shape = (self.width, self.height, 3)
        self.observation_space = spaces.Box(low = 0, 
                                            high = 255,
                                            shape= self.observation_shape,
                                            dtype = np.int8)
        
        self.action_space = spaces.Discrete(9)
        self.window = None
        self.clock = None

        self.agent_dead = False

    def _get_obs(self):
        canvas = pygame.Surface(self.window_size)
        canvas.fill((255, 255, 255))


        # Now we draw the agent
        
        for p in self.agents:
            p.draw(canvas)

        for b in self.bullets:
            b.draw(canvas)

        for e in self.enemies:
            e.draw(canvas)

        return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
    
        pass
    
    def _get_reward(self):
        return 0 if self.agent_dead else 1

    def _get_info(self):
        b5 = self._choose_nearest_bullets()
        agent = self.agents[0]
        return {
            "agent": agent,
            "bullets": b5
        }

    def _update_state(self,action):

        for p in self.agents:
            p.move(action)

        target = [self.agents[0].x, self.agents[0].y]

        for e in self.enemies:
            e.move()
            if(e.shoot_wait == e.shoot_frequency):
                self.bullets.extend(e.shoot(target))

        b2 = []
        for b in self.bullets:
            b.move()
            if(b.check_bounds()):
                b2.append(b)

        self.bullets = b2



        pass

    def _choose_nearest_bullets(self):
        b5 = []
        for b in self.bullets:
            b.color = (255,0,0)
        agent = self.agents[0]
        for _ in range(1):
            best = None
            best_d = self.width**2
            for b in self.bullets:
                d = agent.calc_distance_to([b.x,b.y])
                if( d < best_d and not b in b5):
                    best = b
                    best_d = d

            if best:
                best.color = (255,0,255)
                b5.append(best)

        return b5

    def step(self, action):        
        self._update_state(action)

        agent = self.agents[0]

        for b in self.bullets:
            if(agent.check_collision(b)):
                self.agent_dead = True
                break

        terminated = self.agent_dead
        truncated = False
        return self._get_obs(), self._get_reward(), terminated, truncated, self._get_info()


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.agent_dead = False
        self.enemies = [Enemy(self.map_bounds,'x'),Enemy(self.map_bounds,'+'),Enemy(self.map_bounds,'.')]
        self.agents = [Agent(self.map_bounds)]
        self.bullets = []

        return self._get_obs(), self._get_info()
    
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        else:
            self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(self.window_size)
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface(self.window_size)
        canvas.fill((255, 255, 255))


        # Now we draw the agent
       
        for p in self.agents:
            p.draw(canvas)

        for b in self.bullets:
            b.draw(canvas)

        for e in self.enemies:
            e.draw(canvas)


        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
            # return np.array(pygame.surfarray.pixels3d(canvas))
            