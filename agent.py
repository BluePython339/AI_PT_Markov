import pygame as pg
import config


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((config.tilesize, config.tilesize))
        self.image.fill(config.playercolor)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x, self.y)

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
        if self.on_goal():
            pg.display.set_caption("GOAL ACHIEVEDDDDDDD")
            if config.Q_learning:
                config.on_goal = True
            else:
                self.game.playing = False

    def teleport(self ,x, y):
        self.x = x
        self.y = y

    def up(self):
        self.move(dy=-1)

    def down(self):
        self.move(dy=1)

    def left(self):
        self.move(dx=-1)

    def right(self):
        self.move(dy=1)

    def on_goal(self):
        for goal in self.game.goals:
            if goal.get_pos() == self.get_pos():
                return True
        return False

    def on_trap(self):
        for trap in self.game.traps:
            if trap.get_pos() == self.get_pos():
                print('Traps are gay')



    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                #self.game.lwall = True
                return True
        return False

    def update(self):
        self.rect.x = self.x * config.tilesize
        self.rect.y = self.y * config.tilesize