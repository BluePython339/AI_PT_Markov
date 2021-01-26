import pygame as pg
import sys
import config
from agent import *
from objects import *
from Markov import *
import time

class Game:
    def __init__(self):
        pg.init()
        self.grid = []
        self.lwall = False
        self.goal_pos = (0,0)
        self.screen = pg.display.set_mode((config.width, config.height))
        pg.display.set_caption("Markov game")
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        pass

    def get_policy(self, max_lim, delta):
        transitions = {'frontstep': 0.7, 'sidestep': 0.2, 'backstep': 0.1}
        AI = MarkovDecisionProblem(self, 0.7, transitions)
        v, p = AI.value_itteration(max_lim, delta)
        return self.convert_to_steps(p)





    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        self.traps = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        for row, tiles in enumerate(config.map_data):
            tcol = []
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'G':
                    self.goal_pos = (col, row)
                    Goal_tile(self, col, row)
                if tile == 'T':
                    Trap_tile(self, col, row)
                if tile != '\n':
                    tcol.append(tile)
            self.grid.append(tcol)

    def play(self, policy):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(config.fps) / 1000
            self.player.move(*policy[self.player.x][ self.player.y])
            self.update()
            self.draw()
            time.sleep(1)

    def convert_to_steps(self, policy):
        final =[]
        for i in policy:
            row = []
            for a in i:
                row.append((a[0],a[1]))
            final.append(row)
        return final

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(config.fps) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, config.width, config.tilesize):
            pg.draw.line(self.screen, config.linecolor, (x, 0), (x, config.height))
        for y in range(0, config.height, config.tilesize):
            pg.draw.line(self.screen, config.linecolor, (0, y), (config.width, y))

    def draw(self):
        self.screen.fill(config.bgcolor)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

def read_config(filename):
    map_data = []
    with open(filename, 'r') as f:
        data = f.readlines()
        dimensions = data[0]
        config.height = int(dimensions.split(' ')[0])
        config.width = int(dimensions.split(' ')[1])
        config.tilesize = int(data[1])
        config.bgcolor = tuple([int(i) for i in data[2].split(" ")])
        config.linecolor = tuple([int(i) for i in data[3].split(" ")])
        config.playercolor = tuple([int(i) for i in data[4].split(" ")])
        config.wallcolor = tuple([int(i) for i in data[5].split(" ")])
        config.goalcolor = tuple([int(i) for i in data[6].split(" ")])
        config.trapcolor = tuple([int(i) for i in data[7].split(" ")])
        config.map_data = data[8:]

if __name__ == "__main__":
    read_config('example1')
    g = Game()
    #g.show_start_screen()

    g.new()
    policy = g.get_policy(20, 0.01)
    g.play(policy)
    #g.run()
    #g.show_go_screen()