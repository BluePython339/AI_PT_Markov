from config import *
import numpy as np

class MarkovDecisionProblem():


    def __init__(self, game, discount, transitions):
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
            return -0.4
        elif self.grid[pos] == 'P':
            return -0.4
        elif self.grid[pos] == 'T':
            return -1
        elif self.grid[pos] == 'G':
            return 10

    def calc_val(self,x,y,dx,dy,V):
        res = 0
        fpos = (dx+x, dy+y)
        pos = (x,y)
        lMove, rMove, bMove = self.get_fpos(dx,dy, pos)
        #print("future postion is: {}".format(fpos))
        if self.valid_move(*lMove):
            #print("leftMove is: {}".format(lMove))
            res += self.probs.get('sidestep')*(self.get_reward(lMove))+(self.discounter*V[lMove])
        if self.valid_move(*rMove):
            #print("rightMove is: {}".format(rMove))
            res += self.probs.get('sidestep') * (self.get_reward(rMove) + (self.discounter * V[rMove]))
        if self.valid_move(*bMove):
            #print("backstep is: {}".format(bMove))
            res += self.probs.get('backstep')*(self.get_reward(bMove)+(self.discounter*V[bMove]))
        res += self.probs.get('frontstep')*(self.get_reward(fpos)+(self.discounter*V[fpos]))
        return res

    #implement value itteration
    def value_itteration(self, max_lim, delta):
        k = 0
        term  = False
        gridshape = np.shape(self.grid)
        print(gridshape)
        V = np.zeros(gridshape)
        V[self.goalx,self.goaly] = 1.0
        p = np.full(gridshape, 0 , dtype='i,i') #grid of shape gridshape filled with (0,0)
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
                            a = (self.calc_val(*pos, *dir, V),dir)
                            #print("Q value of this move: {}".format(a))
                            vals.append(a)
                        #print('\n'*1)
                    if not vals:
                        vals.append((np.NINF, (0,0)))
                    ulti = max(vals, key= lambda i: i[0])
                    p[pos] = ulti[1]
                    v[pos] = ulti[0]
                #print(v)
                #a = input("press enter to continue...")
            #print("Goal located at: {}".format((self.goalx, self.goaly)))
            #v[self.goalx,self.goaly] = 1.0
            #print(v)
            #input("press enter to continue to policy execution...")
            p[self.goalx,self.goaly] = (2,2)
            if np.allclose(V,v, atol=delta):
                term = True
            else:
                V = v
        with open("resv", 'w+') as a:
            for i in v[::-1]:
                a.write("|||".join(map(str, i))+'\n')
            a.write("\n"*3)
            for i in p[::-1]:
                a.write("|".join(map(str, i))+'\n')

            a.write("\n" * 3)
            for i in self.grid:
                a.write("|".join(map(str, i)) + '\n')
        return v, p

    #values kloppen maar lijken gespiegeld?
    #kijk in resv


    #implement q-learning
    def q_learning(self):
        pass



