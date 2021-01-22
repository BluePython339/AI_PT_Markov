from config import *


class MarkovDecisionProblem():


    def __init__(self, game):
        self.game = game
        self.grid = game.grid
        self.goalx, self.goaly = game.goal_pos
        self.startx = game.playing.x
        self.starty = game.playing.y
        self.prevx = self.startx
        self.prevy = self.startx
        self.currentx = self.startx
        self.currenty = self.starty
        self.determ = False
        self.prevA
        self.movevount = 0
        self.params ={
            "Corr" : 0,
            "Side" : 0,
            "Back" : 0,
            "Nost" : 1
        }
        self.treward = 0

    def get_reward(self):
        if not self.game.playing:
            return 10
        elif abs((self.goalx - self.currentx) + (self.goaly - self.currenty) ) < abs((self.goalx - self.prevy) + (self.goaly - self.prevy) ):
            return 1
        elif abs((self.goalx - self.currentx) + (self.goaly - self.currenty) ) == abs((self.goalx - self.prevy) + (self.goaly - self.prevy) ):
            if self.game.lwall:
                self.game.lwall = False
                return -0.6
            else:
                return -0.4
        else:
            return -1

    def move(self, action):
        if self.determ:
            if action == "UP":
                self.game.player.up()
            if action == "DOWN":
                self.game.player.down()
            if action == "LEFT":
                self.game.player.left()
            if action == "RIGHT":
                self.game.player.right()
        else:
            pass



