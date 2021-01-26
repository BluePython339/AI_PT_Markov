import pygame as pg
import config

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((config.tilesize, config.tilesize))
        self.image.fill(config.wallcolor)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * config.tilesize
        self.rect.y = y * config.tilesize

    def get_pos(self):
        return (self.x, self.y)

class Goal_tile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.weight = 100
        self.groups = game.all_sprites, game.goals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((config.tilesize, config.tilesize))
        self.image.fill(config.goalcolor)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.reward = 1
        self.rect.x = x * config.tilesize
        self.rect.y = y * config.tilesize

    def get_pos(self):
        return (self.x, self.y)

class Trap_tile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.weight = -10
        self.groups = game.all_sprites, game.traps
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((config.tilesize, config.tilesize))
        self.image.fill(config.trapcolor)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * config.tilesize
        self.rect.y = y * config.tilesize

    def get_pos(self):
        return (self.x, self.y)