from config import *
import numpy as np
import copy
import config
import random

class MarkovDecisionProblem():


    def __init__(self, game, discount, transitions=None):
        self.game = game
        self.grid = np.array(game.grid)
        self.goalx, self.goaly = game.goal_pos
        self.directions = [(-1,0),(0,-1),(1,0),(0,1)]
        self.probs = transitions
        self.discounter = discount


    def valid_move(self, x, y, dx=0, dy=0):
        try:
            #print(self.grid[x + dx][y + dy])
            if self.grid[x+dx][y+dy] != '1':
                return True
            return False
        except Exception:
            print("yes")
            return False

    def sum_tuple(self, fst, snd):
        return tuple(map(lambda i, j: i + j, fst, snd))

    def get_fpos(self,dx,dy, pos):
        if dx == 1:
            bMove = self.sum_tuple((-1,0), pos)
            lMove = self.sum_tuple((0,1), pos)
            rMove = self.sum_tuple((0, -1), pos)
            return lMove,rMove,bMove
        elif dx == -1:
            bMove = self.sum_tuple((1,0), pos)
            lMove = self.sum_tuple((0,-1), pos)
            rMove = self.sum_tuple((0, 1), pos)
            return lMove, rMove, bMove
        elif dy == 1:
            bMove = self.sum_tuple((0,-1), pos)
            lMove = self.sum_tuple((-1,0), pos)
            rMove = self.sum_tuple((1,0), pos)
            return lMove, rMove, bMove
        else:
            bMove = self.sum_tuple((0,1), pos)
            lMove = self.sum_tuple((-1,0), pos)
            rMove = self.sum_tuple((1,0), pos)
            return lMove, rMove, bMove

    def get_reward(self, pos):
        if self.grid[pos] == '.':
            return -0.04
        elif self.grid[pos] == 'P':
            return -0.04
        elif self.grid[pos] == 'T':
            return -1
        elif self.grid[pos] == 'G':
            return 1

    def calc_val3(self, x,y,dx,dy,V):
        res = 0
        fpos = (dx+x, dy+y)
        pos = (x,y)
        lMove, rMove, bMove = self.get_fpos(dx, dy, pos)
        res += -0.04
        if self.valid_move(*lMove):
            #print("leftMove is: {}".format(lMove))
            res += self.probs.get('sidestepL')*(self.discounter*V[lMove])
        if self.valid_move(*rMove):
            #print("rightMove is: {}".format(rMove))
            res += self.probs.get('sidestepR') * + (self.discounter * V[rMove])
        if self.valid_move(*bMove):
            #print("backstep is: {}".format(bMove))
            res += self.probs.get('backstep')*(self.discounter*V[bMove])
        res += self.probs.get('frontstep')*(self.discounter*V[fpos])
        return res

    def calc_val2(self, x,y,dx,dy,V):
        res = 0
        fpos = (dx+x, dy+y)
        pos = (x,y)
        lMove, rMove, bMove = self.get_fpos(dx, dy, pos)
        res += self.get_reward(pos)
        if self.valid_move(*lMove):
            #print("leftMove is: {}".format(lMove))
            res += self.probs.get('sidestepL')*(self.discounter*V[lMove])
        if self.valid_move(*rMove):
            #print("rightMove is: {}".format(rMove))
            res += self.probs.get('sidestepR') * + (self.discounter * V[rMove])
        if self.valid_move(*bMove):
            #print("backstep is: {}".format(bMove))
            res += self.probs.get('backstep')*(self.discounter*V[bMove])
        res += self.probs.get('frontstep')*(self.discounter*V[fpos])
        return res

    #implement value itteration
    def value_itteration(self, max_lim, delta):
        k = 0
        term  = False
        gridshape = np.shape(self.grid)
        V = np.zeros(gridshape)
        print(V.shape)
        V[self.goalx,self.goaly] = 1
        for i in self.game.traps:
            V[i.get_pos()] = -10
        p = np.full(gridshape, 0 , dtype='i,i') #grid of shape gridshape filled with (0,0)
        print(V)
        while k <= max_lim and not term:
            k +=1
            print(k)
            v = np.zeros(gridshape)
            for pos in np.ndindex(V.shape):
                #print("current pos: {}".format(pos))
                if self.grid[pos] == "1":
                    #print("this is a wall")
                    #print('\n'*1)
                    v[pos] = np.NINF
                    p[pos] = (0,0)
                else:
                    vals = []
                    for dir in self.directions:
                        #print("now checking direction: {}".format(dir))
                        if self.valid_move(*pos, *dir):
                            #print("this is a valid move")
                            a = (self.calc_val3(*pos, *dir, V),dir)
                            #print("Q value of this move: {}".format(a))
                            vals.append(a)
                    ulti = max(vals, key= lambda i: i[0])
                    p[pos] = ulti[1]
                    v[pos] = ulti[0]
            v[self.goalx,self.goaly] = 10
            p[self.goalx,self.goaly] = (0,0)
            if np.allclose(V,v, atol=delta):
                term = True
            else:
                V = copy.deepcopy(v)
        with open("resv", 'w+') as a:
            a.write(str(v))
            a.write("\n"*3)
            a.write(str(p))
            a.write("\n" * 3)
            a.write(str(self.grid))
        return v, p #np.rot90(np.flip(p,1),k=1)

    #values kloppen maar lijken gespiegeld?
    #kijk in resv

    def Qmax(self, x, y,dx,dy,V, a):
        g = self.discounter
        fpos = (dx + x, dy + y)
        pos = (x, y)
        res = 0
        lMove, rMove, bMove = self.get_fpos(dx, dy, fpos)
        Qall = [lMove, rMove, self.sum_tuple(fpos, (dx,dy))]
        QValid =[]
        for i in Qall:
            if self.valid_move(*i):
                QValid.append(i)
        Qmax = max(QValid, key =lambda i : V[i])
        res += self.get_reward(Qmax)+(g*V[Qmax])-V[pos]
        res *= a
        res += V[pos]
        return res, fpos




    def egreedy(self, V, s):
        moves = []
        for i in self.directions:
            if self.valid_move(*self.sum_tuple(i,s)):
                moves.append((i,V[self.sum_tuple(i,s)]))

        Pmax = max(moves, key= lambda i : i[1])
        moves.remove(Pmax)
        Pe = random.choice(moves)
        return Pmax[0], Pe[0]



    #implement q-learning
    def q_learning(self, e ,a,startstate):
        e = np.float32(e)
        V = np.zeros(self.grid.shape)
        V[self.goalx,self.goaly] = 10
        for i in self.game.traps:
            V[i.get_pos()] = -1
        s = startstate
        first_update = False
        thdns = 0
        tick = 0
        tgoals = 0
        goals = 0
        gstate = (self.goalx,self.goaly)

        data = {}
        for pos in np.ndindex(V.shape):
            data[str(pos)] = 0
        while goals < 140:
            if tgoals > 100000:
                break
            if tick == 1000:
                thdns +=1
                tgoals += goals
                print("Total {} Goals in {} Thousand itters".format(tgoals,thdns))
                goals = 0
                tick = 0
            if s == gstate:
                s = startstate
                goals += 1
            Pmax, Pe = self.egreedy(V, s)
            if random.randint(0, 1) <= e:
                Q_val, fpos = self.Qmax(*s, *Pe, V, a)
                move = Pe
            else:
                Q_val, fpos = self.Qmax(*s, *Pmax, V, a)
                move = Pmax
            data[str(s)] +=1
            V[s] = Q_val
            s = fpos

            if e > 0:
                e -= 0.0005
            else:
                e = 0

            tick+=1

        s = startstate
        for i in V:
            fin = ""
            for a in i:
                fin += "{:.2f}".format(a)
                fin += " , "
            print(fin)
        for i in data:
            print("position: {}  times visited {}".format(i, data.get(i)))

        while True:
            if s == gstate:
                s = startstate
                #print('yay')
            if tick == 1000:
                thdns +=1
                #print("{} Goals in {} Thousand itters".format(goals,thdns))
                goals = 0
                tick = 0
            if config.on_goal:
                goals += 1
                s = startstate
                self.game.player.teleport(*s)
                config.on_goal = False
            Pmax, Pe = self.egreedy(V, s)
            #print("PMAX: {}, PE{}, Epsilon {}".format(Pmax, Pe, e))
            if random.randint(0,1) <= e:
                Q_val, fpos = self.Qmax(*s,*Pe,V,a)
                move = Pe
            else:
                Q_val, fpos = self.Qmax(*s,*Pmax,V,a)
                move = Pmax
            if Q_val > V[s]:
                V[s] = Q_val
            s = fpos
            tick +=1
            yield move, V









