import numpy as np
import copy
import random
import math
import time
import csv

# weights table, it's a ponderation of the manhattan distance
tp = np.array([[36, 12, 12, 4, 1, 1, 4, 1, 0],
               [8, 7, 6, 5, 4, 3, 2, 1, 0],
               [8, 7, 6, 5, 4, 3, 2, 1, 0],
               [8, 7, 6, 5, 3, 2, 4, 1, 0],
               [8, 7, 6, 5, 3, 2, 4, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 0]
               ])
tp2 = np.array([[36, 12, 12, 4, 1, 1, 4, 1, 0],
                [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                [8, 7, 6, 5, 3, 2, 4, 1, 0],
                [8, 7, 6, 5, 3, 2, 4, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
                ])
tp3 = np.array([[],
                [24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                [24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                [],
                [],
                []
                ])
# coefficients to reduce the value of the evaluation function
coef_normal = (1, 4)


class Puzzle:

    # creating the puzzle
    def __init__(self, n):
        self.size = n
        self.state = (np.arange(0, n * n).reshape(n, n)).astype(object)
        self.state[n - 1][n - 1] = 'X'
        self.path = ""
        self.f = 0

    def __eq__(self, other):
        if isinstance(other, self.__class__):

            for i in range(0, self.size):
                for j in range(0, self.size):
                    if (self.state[i][j] != other.state[i][j]):
                        return False
            return True

        return False

    # verification of a goal state
    def isGoal(self):
        return self == Puzzle(self.size)

    # a function that permits to move a square in the puzzle in a certain direction
    def move(self, direction):
        ij = np.argwhere(self.state == 'X')
        i = ij[0][0]
        j = ij[0][1]

        if (direction == "O"):
            if (j > 0):
                tc = copy.deepcopy(self)
                tc.state[i][j] = tc.state[i][j - 1]
                tc.state[i][j - 1] = 'X'
                tc.path += "O"
                return tc
            else:
                return None

        elif (direction == "E"):
            if (j < self.size - 1):
                tc = copy.deepcopy(self)
                tc.state[i][j] = tc.state[i][j + 1]
                tc.state[i][j + 1] = 'X'
                tc.path += "E"
                return tc
            else:
                return None

        elif (direction == "N"):
            if (i > 0):
                tc = copy.deepcopy(self)
                tc.state[i][j] = tc.state[i - 1][j]
                tc.state[i - 1][j] = 'X'
                tc.path += "N"
                return tc
            else:
                return None

        else:

            if (i < self.size - 1):
                tc = copy.deepcopy(self)
                tc.state[i][j] = tc.state[i + 1][j]
                tc.state[i + 1][j] = 'X'
                tc.path += "S"
                return tc
            else:
                return None

    def generateKids(self):

        states_list = []
        states_list.append(self.move("N"))
        states_list.append(self.move("S"))
        states_list.append(self.move("E"))
        states_list.append(self.move("O"))
        l = [i for i in states_list if i is not None]  ##delete the none from the children

        return l

    def shuffle(self):
        s = 0
        if self.size == 3:
            s = 100;
        elif self.size == 4:
            s = 60;
        else:
            s = 80
        for i in range(s):
            r = random.choice('NSEO')
            new = self.move(r)
            if (new != None):  # the case where a move can't be done
                self = new
        self.path = ''  # reset the path cuz the move function updates it

        return self

    # gets the distance between a position of a square and it's right position at a goal state
    def elementaryDistance(self, i):
        # recuperer les coordonnees de i dans l'état
        cor_xy = np.argwhere(self.state == i)
        cor_x = cor_xy[0][0]
        cor_y = cor_xy[0][1]

        # gets the coordinates of the i square at the goal state
        final_puzzle = Puzzle(self.size).state
        cor_xy_final = np.argwhere(final_puzzle == i)
        cor_x_final = cor_xy_final[0][0]
        cor_y_final = cor_xy_final[0][1]

        # calculer le nombre de deplacement elemenetaire pour metrre i à la position final
        elt_dist = abs(cor_x_final - cor_x) + abs(cor_y_final - cor_y)
        return elt_dist

    # heuristic calculation
    def h(self, k):
        heuristic = 0

        if k == 7:
            # recuperer les coordonnees de i dans l'état
            a = 0
            for i in range(self.size * self.size - 1):

                cor_xy = np.argwhere(self.state == i)
                cor_x = cor_xy[0][0]
                cor_y = cor_xy[0][1]

                # gets the coordinates of the i square at the goal state
                final_puzzle = Puzzle(self.size).state
                cor_xy_final = np.argwhere(final_puzzle == i)
                cor_x_final = cor_xy_final[0][0]
                cor_y_final = cor_xy_final[0][1]

                # calculer le nombre de deplacement elemenetaire pour metrre i à la position final
                if cor_x != cor_x_final:
                    a += 1
            b = 0
            for i in range(self.size * self.size - 1):

                cor_xy = np.argwhere(self.state == i)
                cor_x = cor_xy[0][0]
                cor_y = cor_xy[0][1]

                # gets the coordinates of the i square at the goal state
                final_puzzle = Puzzle(self.size).state
                cor_xy_final = np.argwhere(final_puzzle == i)
                cor_x_final = cor_xy_final[0][0]
                cor_y_final = cor_xy_final[0][1]

                # calculer le nombre de deplacement elemenetaire pour metrre i à la position final
                if cor_y != cor_y_final:
                    b += 1

            return a + b

        if k == 8:
            # recuperer les coordonnees de i dans l'état
            a = 0
            for i in range(self.size * self.size - 1):

                cor_xy = np.argwhere(self.state == i)
                cor_x = cor_xy[0][0]
                cor_y = cor_xy[0][1]

                # gets the coordinates of the i square at the goal state
                final_puzzle = Puzzle(self.size).state
                cor_xy_final = np.argwhere(final_puzzle == i)
                cor_x_final = cor_xy_final[0][0]
                cor_y_final = cor_xy_final[0][1]

                # calculer le nombre de deplacement elemenetaire pour metrre i à la position final
                elt_dist = abs(cor_x_final - cor_x) + abs(cor_y_final - cor_y)
                if elt_dist != 0:
                    a += 1
            return a

        if self.size < 4:
            heuristic = sum(
                tp[k - 1][i] * self.elementaryDistance(i) for i in range(len(self.state) * len(self.state) - 1))
        elif self.size == 4 and (k == 2 or k == 3):
            heuristic = sum(
                tp2[k - 1][i] * self.elementaryDistance(i) for i in range(len(self.state) * len(self.state) - 1))
        elif self.size == 5 and (k == 2 or k == 3):
            heuristic = sum(
                tp3[k - 1][i] * self.elementaryDistance(i) for i in range(len(self.state) * len(self.state) - 1))
        else:
            heuristic = sum(self.elementaryDistance(i) for i in range(len(self.state) * len(self.state) - 1))

        heuristic /= coef_normal[k % 2]

        return heuristic;

    def evaluation(self, k):
        return len(self.path) + self.h(k)


def hashit(puzzle):
    return hash(str(puzzle.state))


class Border:

    def __init__(self):
        self.states = list()

    def add(self, o):

        t = len(self.states)
        if t == 0:
            self.states.append(o)

        else:
            cond = False
            for i in range(t):
                if self.states[i].f >= o.f and not cond:
                    self.states.insert(i, o)
                    cond = True

            if not cond:
                self.states.insert(t, o)


def solve(taquin, k):
    if taquin.size == 4 or taquin.size == 5:
        if k != 2 and k != 3 and k != 7 and k != 8 and k != 6:
            print("the puzzle can't be solved using the heuritsic h", k)
            return None
    maxExploredSize = 0
    borderSize = 0
    if taquin.isGoal():
        return taquin

    bd = Border()
    explored = {}

    bd.add(taquin)

    st = time.time()
    while bd.states:
        # check one element of the border
        s = bd.states.pop(0)
        borderSize += 1
        # check if it's a goal state
        if s.isGoal() == True:
            print("Exlored states size = ", maxExploredSize)
            print("border size = ", borderSize)
            print("%s steps  taken : %s " % (len(s.path), s.path))
            t = time.time() - st
            print("time taken : ", t)
            return [s, maxExploredSize, borderSize, t]

        explored[hashit(s)] = s.evaluation(k)

        maxExploredSize += 1
        # we get all the children from the state of all the possible actions
        kids = s.generateKids()

        for child in kids:
            h = hashit(child)
            if h in explored:
                continue

            child.f = child.evaluation(k)

            if (child not in bd.states):
                bd.add(child)
                borderSize += 1
            else:
                indice_i = bd.states.index(child)
                if (child.f < bd.states[indice_i].f):
                    bd.add(child)
                    borderSize += 1

            # si l'état existe, on le remplace si le nouveau f < à l'ancien
            # remplacer dans l'ens explore

    return None


def getnpos(td, tf):
    ch = tf.path
    l = list()
    for i in ch:
        cor_xy_final = np.argwhere(td.state == 'X')
        x = cor_xy_final[0][0]
        y = cor_xy_final[0][1]

        if (i == 'N'):
            l.append(td.state[x - 1][y])
            td = td.move('N')
        if (i == 'S'):
            l.append(td.state[x + 1][y])
            td = td.move('S')
        if (i == 'E'):
            l.append(td.state[x][y + 1])
            td = td.move('E')
        if (i == 'O'):
            l.append(td.state[x][y - 1])
            td = td.move('O')

    return l


def taquinAvecEtat(n, l):
    t = Puzzle(n)
    for i in range(n):
        for j in range(n):
            el = l.pop(0);
            t.state[i][j] = el if el == 'X' else int(el)

    return t

