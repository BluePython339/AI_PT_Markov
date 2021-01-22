import pygame as pg
import time
import itertools
import config
from agent import Agent

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800

colors =itertools.cycle((pg.Color("green"),pg.Color("white"),pg.Color("red"),pg.Color("blue")))

class Frame(object):

    def __init__(self,mapfile):
        pg.init()
        pg.display.set_caption("MARKOV_PROBLEM")
        self.height = 0
        self.width  = 0
        self.tile_size = 0
        self.mapfile = mapfile
        self.grid = []
        self.read_map()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.width,self.height))
        self.surface = pg.Surface((self.width, self.height))
        self.screen.fill(config.bgcolor)
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.agent = Agent(self,0,0)




    def read_map(self):
        with open(self.mapfile, 'r') as f:
            data = f.readlines()
            dimensions = data[0]
            self.height = int(dimensions.split(' ')[0])
            config.height = self.height
            self.width = int(dimensions.split(' ')[1])
            config.width = self.width
            self.tile_size = int(data[1])
            self.bgcolor = tuple([int(i) for i in data[2].split(" ")])
            config.bgcolor = self.bgcolor
            self.linecolor = tuple([int(i) for i in data[3].split(" ")])
            config.linecolor = self.linecolor
            self.playercolor = tuple([int(i) for i in data[4].split(" ")])




    def draw_grid(self):
        for x in range(0, self.width, self.tile_size):
            pg.draw.line(self.surface, self.linecolor, (x, 0), (x, self.height))
        for y in range(0, self.height, self.tile_size):
            pg.draw.line(self.surface, self.linecolor, (0, y), (self.width, y))


    def draw(self):
        self.draw_grid()
        self.all_sprites.draw(self.surface)

        self.screen.blit(self.surface,(0,0))
        pg.display.flip()

    def run(self):
        runin = True
        while runin:
                self.draw()
                #self.clock.tick(120)
                time.sleep(10)

