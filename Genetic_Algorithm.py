from __builtin__ import str

from random import *
import copy
from time import *
import math
from PySide import QtCore

ROULETTE = 1
FILL_NEXT_GENERATION = 2

CHILD_FLIP = 10
CHILD_SPLIT = 11
CHILD_FLIP2 = 12
CHILD_MEAN = 13



class B(Exception):
    pass


class GenecticException(B):
    what = None


class chromosome_t():
    def __init__(self, n_chromosomes, maxvalue = None, minvalue = 0, chromosomes_is_float = False, ):
        self.N_CHRO = n_chromosomes
        if maxvalue is None:
            self.MAXVALUE = n_chromosomes
        else:
            self.MAXVALUE = maxvalue
        self.MINVALUE = minvalue
        self.CHRO_IS_F = chromosomes_is_float


class GeneticAlgorithm:
    """
The structure of a tuple of the PULL is:
[individual, FITNNES, PROBABILITY FOR THE ROULETTE]

The structure of a individual is:
[value,value,value,...,value] It has as many values as chromosomes.

Ways to Generate Children:

    fatherx [1, 2, 3]  -->  r_fatherx [3, 2, 1]

    CHILD_FLIP
        father[1, 6, 7, 2, 6, 8, 2, 1, 5, 6, 3, 8, 7]
                          [    father   ]

        child [1, 6, 7, 2, 5, 1, 2, 8, 6 ,6 ,3, 8, 7]
                          [   r_father  ]
    CHILD_SPLIT
        father1[1, 6, 7, 2, 6, 8, 2, 1, 5, 6, 3, 8, 7]
               [   father1_1    ][     father1_2     ]

        father1[5, 4, 8, 6, 3, 2, 8, 6, 5, 7, 9, 3, 7]
               [   father2_1    ][     father2_2     ]

        child1 [1, 6, 7, 2, 6, 8, 8, 6, 5, 7, 9, 3, 7]
               [   father1_1    ][     father2_2     ]

        child2 [5, 4, 8, 6, 3, 2, 2, 1, 5, 6, 3, 8, 7]
               [   father2_1    ][     father1_2     ]

    CHILD_FLIP2
        father[1, 6, 7, 2, 6, 8, 2, 1, 5, 6, 3, 8, 7]
              [ father_1 ][   father_2  ][ father_3 ]

        child1[1, 6, 7, 2, 5, 1, 2, 8, 6 ,6 ,3, 8, 7]
              [ father_1 ][  r_father_2 ][ father_3 ]

        child2[2, 7, 6, 1, 6, 8, 2, 1, 5, 7, 8, 3, 6]
              [r_father_1][   father_2  ][r_father_3]
        return the best [father, child1, child2]

    CHILD_MEAN and chromosomes_is_float = True
        father1 [1, 5, 7, 6]

        father2 [3, 8, 1, 3]

        child   [2, 6.5, 4, 4.5]  child[i] = (father1[i]+father2[i])/2

    CHILD_MEAN and chromosomes_is_float = False
        father1 [1, 5, 7, 6]

        father2 [3, 8, 1, 3]

        child   [2, 6, 4, 4]  child[i] = floor((father1[i]+father2[i])/2)

Example:
This is the typical travelling salesman problem (TSP) in this case there are 20 cities.

from Genetic_Algorithm import *


ELITISM = 10
MUTE = 2
REVERSE = True
SELECTION_TYPE = FILL_NEXT_GENERATION
SIZE_PULL = 1000
N_CHROMOSOMES = 20
HIGH_LOW = False
ITMAX = 100
TYPECHILD = CHILD_FLIP
distance = [[9.22337203685e+18, 77.0, 30.0, 52.0, 30.0, 28.0, 28.0, 91.0, 35.0, 26.0, 61.0, 56.0, 27.0, 44.0, 35.0, 71.0, 55.0, 58.0, 30.0, 74.0] ,
            [77.0, 9.22337203685e+18, 41.0, 39.0, 82.0, 64.0, 72.0, 99.0, 89.0, 28.0, 40.0, 64.0, 72.0, 86.0, 86.0, 82.0, 94.0, 33.0, 64.0, 42.0] ,
            [30.0, 41.0, 9.22337203685e+18, 22.0, 37.0, 32.0, 39.0, 22.0, 83.0, 41.0, 92.0, 77.0, 88.0, 46.0, 55.0, 28.0, 23.0, 56.0, 21.0, 60.0] ,
            [52.0, 39.0, 22.0, 9.22337203685e+18, 49.0, 55.0, 90.0, 94.0, 24.0, 22.0, 74.0, 26.0, 72.0, 26.0, 36.0, 93.0, 61.0, 98.0, 69.0, 49.0] ,
            [30.0, 82.0, 37.0, 49.0, 9.22337203685e+18, 30.0, 61.0, 55.0, 65.0, 26.0, 23.0, 73.0, 77.0, 99.0, 35.0, 82.0, 41.0, 90.0, 93.0, 60.0] ,
            [28.0, 64.0, 32.0, 55.0, 30.0, 9.22337203685e+18, 42.0, 83.0, 39.0, 36.0, 24.0, 95.0, 55.0, 98.0, 20.0, 58.0, 92.0, 95.0, 91.0, 30.0] ,
            [28.0, 72.0, 39.0, 90.0, 61.0, 42.0, 9.22337203685e+18, 61.0, 54.0, 28.0, 91.0, 77.0, 55.0, 62.0, 96.0, 31.0, 23.0, 91.0, 49.0, 100.0] ,
            [91.0, 99.0, 22.0, 94.0, 55.0, 83.0, 61.0, 9.22337203685e+18, 43.0, 100.0, 46.0, 65.0, 90.0, 60.0, 63.0, 80.0, 69.0, 39.0, 60.0, 62.0] ,
            [35.0, 89.0, 83.0, 24.0, 65.0, 39.0, 54.0, 43.0, 9.22337203685e+18, 31.0, 97.0, 56.0, 93.0, 94.0, 39.0, 33.0, 32.0, 46.0, 94.0, 92.0] ,
            [26.0, 28.0, 41.0, 22.0, 26.0, 36.0, 28.0, 100.0, 31.0, 9.22337203685e+18, 70.0, 81.0, 22.0, 43.0, 21.0, 72.0, 99.0, 70.0, 38.0, 98.0] ,
            [61.0, 40.0, 92.0, 74.0, 23.0, 24.0, 91.0, 46.0, 97.0, 70.0, 9.22337203685e+18, 73.0, 69.0, 59.0, 71.0, 64.0, 78.0, 66.0, 42.0, 80.0] ,
            [56.0, 64.0, 77.0, 26.0, 73.0, 95.0, 77.0, 65.0, 56.0, 81.0, 73.0, 9.22337203685e+18, 73.0, 28.0, 36.0, 91.0, 64.0, 68.0, 30.0, 26.0] ,
            [27.0, 72.0, 88.0, 72.0, 77.0, 55.0, 55.0, 90.0, 93.0, 22.0, 69.0, 73.0, 9.22337203685e+18, 79.0, 73.0, 43.0, 87.0, 65.0, 30.0, 27.0] ,
            [44.0, 86.0, 46.0, 26.0, 99.0, 98.0, 62.0, 60.0, 94.0, 43.0, 59.0, 28.0, 79.0, 9.22337203685e+18, 88.0, 40.0, 39.0, 68.0, 31.0, 70.0] ,
            [35.0, 86.0, 55.0, 36.0, 35.0, 20.0, 96.0, 63.0, 39.0, 21.0, 71.0, 36.0, 73.0, 88.0, 9.22337203685e+18, 54.0, 58.0, 50.0, 29.0, 63.0] ,
            [71.0, 82.0, 28.0, 93.0, 82.0, 58.0, 31.0, 80.0, 33.0, 72.0, 64.0, 91.0, 43.0, 40.0, 54.0, 9.22337203685e+18, 39.0, 84.0, 49.0, 25.0] ,
            [55.0, 94.0, 23.0, 61.0, 41.0, 92.0, 23.0, 69.0, 32.0, 99.0, 78.0, 64.0, 87.0, 39.0, 58.0, 39.0, 9.22337203685e+18, 68.0, 63.0, 60.0] ,
            [58.0, 33.0, 56.0, 98.0, 90.0, 95.0, 91.0, 39.0, 46.0, 70.0, 66.0, 68.0, 65.0, 68.0, 50.0, 84.0, 68.0, 9.22337203685e+18, 79.0, 87.0] ,
            [30.0, 64.0, 21.0, 69.0, 93.0, 91.0, 49.0, 60.0, 94.0, 38.0, 42.0, 30.0, 30.0, 31.0, 29.0, 49.0, 63.0, 79.0, 9.22337203685e+18, 26.0] ,
            [74.0, 42.0, 60.0, 49.0, 60.0, 30.0, 100.0, 62.0, 92.0, 98.0, 80.0, 26.0, 27.0, 70.0, 63.0, 25.0, 60.0, 87.0, 26.0, 9.22337203685e+18]]
def fitnnes(item):
    dist = 0
    cityant = item[0]
    for cityact in item[1:N_CHROMOSOMES]:
        dist = dist + distance[cityant][cityact]
        cityant = cityact
    dist = dist + distance[cityant][item[0]]
    return dist

if __name__ ==  "__main__":
    print "["
    for x in distance:
        print x[:20], ","
    print "]"
    f = fitnnes
    chro = chromosome_t(N_CHROMOSOMES)
    try:
        GA = GeneticAlgorithm(f, chro, itmax = ITMAX, selection_type = SELECTION_TYPE,
                            High_Low = HIGH_LOW, size_pool = SIZE_PULL, child_type = TYPECHILD, porcent_elitism = ELITISM, porcent_mute = MUTE)
        GA.run()
    except GenecticException:
        print GenecticException.what


        """

    def __init__(self, fun_fitness, chromosomes, itmax = 50, child_type = CHILD_FLIP, selection_type = FILL_NEXT_GENERATION,
                 High_Low = False, size_pool = 1000, porcent_elitism = 10, porcent_mute = 2, can_repeated_chro = False, testing = False):

        if selection_type not in [ROULETTE, FILL_NEXT_GENERATION]:
            a = GenecticException
            a.what = "Error: selection_type is not correct."
            raise a
        if porcent_elitism not in range(100):
            a = GenecticException
            a.what = "Error: porcent_elitism not in range [0,100]"
            raise a
        if porcent_mute not in range(100):
            a = GenecticException
            a.what = "Error: porcent_mute not in range [0,100]"
            raise a
        if High_Low not in [True, False]:
            a = GenecticException
            a.what = "Error: High_Low must be True or False", "Error: fun_fitness is None"
            raise a
        self.__ELITISM = porcent_elitism / 100.0
        self.__MUTE = porcent_mute
        self.__REVERSE = High_Low
        self.__SELECTION_TYPE = selection_type
        self.__SIZE_POOL = size_pool
        self.__N_CHROMOSOMES = chromosomes.N_CHRO
        self.__FUN_FITNESS = fun_fitness
        self.__ITMAX = itmax
        self.__TYPECHILD = child_type
        self.__rangechild = (int)(self.__SIZE_POOL - self.__SIZE_POOL * self.__ELITISM)
        self.__sizeelitism = (int)(self.__SIZE_POOL * self.__ELITISM)
        self.__CHRO_IS_F = chromosomes.CHRO_IS_F
        self.__CHRO_MAXVALUE = chromosomes.MAXVALUE
        self.__CHRO_MINVALUE = chromosomes.MINVALUE
        self.__CAN_REPETEAD_CHRO = can_repeated_chro
        self.__POOL = self.__Generate_pool()
        self.__TEST_POOL = testing  # Flag for testing purpose
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__run)
        self.timer.start(500)


    """
        Function that generate a pool
    """

    def __Generate_pool(self):
        if self.__CHRO_IS_F is False:
            if self.__CAN_REPETEAD_CHRO is False:
                ind = range(self.__CHRO_MINVALUE, self.__CHRO_MAXVALUE)
                new_pool = [[sample(ind, self.__N_CHROMOSOMES), 0, 0] for y in range(self.__SIZE_POOL)]
            else:
                new_pool = [[[randint(self.__CHRO_MINVALUE,self.__CHRO_MAXVALUE)for x in range(self.__N_CHROMOSOMES)], 0, 0] for y in range(self.__SIZE_POOL)]
            return new_pool
        else:
            new_pool = [
                [[uniform(self.__CHRO_MINVALUE, self.__CHRO_MAXVALUE) for x in range(self.__N_CHROMOSOMES)], 0, 0] for y
                in range(self.__SIZE_POOL)]
            return new_pool

    """
        Function that returns a key to sort pool
    """

    def __getKey(self, item):
        return item[1]

    """
        Function that returns a individuos i
    """

    def __Get_Individuos(self, individual):
        if individual not in range(0, self.__SIZE_POOL):
            a = GenecticException
            a.what = "Error: individual", individual, " not existing, 0 < = individual < " + str(self.__SIZE_POOL)
            raise a
        return copy.copy(self.__POOL[individual][0])

    """
        Function that set the Fittnes to sort pool
    """

    def __Set_Fittnes(self, individual, Fittnes):
        if individual not in range(0, self.__SIZE_POOL):
            a = GenecticException
            a.what = "Error: individual", individual, " not existing, 0 < = individual < " + str(self.__SIZE_POOL)
            raise a
        self.__POOL[individual][1] = Fittnes

    """
        Function that sort pool if rever is True sort of highest to lowest else lowest to highest
    """

    def __sort_pool(self, rever = False):
        self.__POOL.sort(key = self.__getKey, reverse = rever)

    """
        Generate a child by flip method
    """

    def __Generate_Child_flip(self, item):
        child = copy.copy(item)
        index = [randint(0, self.__N_CHROMOSOMES - 1), randint(0, self.__N_CHROMOSOMES - 1)]
        index.sort()
        revert = copy.copy(item[index[0]:index[1]])
        child[index[0]:index[1]] = revert[::-1]
        return child

    """
        Generate two sons by flip method, after that it returns the best between Father and the two sons.
    """

    def __Generate_Child_tournament_Det(self, item):
        child = copy.copy(item)
        index = [randint(0, self.__N_CHROMOSOMES - 1), randint(0, self.__N_CHROMOSOMES - 1)]
        index.sort()
        revert = copy.copy(item[index[0]:index[1]])
        child[index[0]:index[1]] = revert[::-1]

        child2 = copy.copy(item)
        revert2left = child2[0:index[0]]
        revert2right = child2[index[1]: self.__N_CHROMOSOMES - 1]
        child2[0:index[0]] = revert2left[::-1]
        child2[index[1]:self.__N_CHROMOSOMES - 1] = revert2right[::-1]

        listIndividual = [item, child, child2]
        return self.__Tournament_Selection_Deterministic(listIndividual)

    """
        Generate two sons by split method
    """

    def __Generate_Child_split(self, item1, item2):
        child1 = copy.copy(item1)
        child2 = copy.copy(item2)
        split = randint(1, self.__N_CHROMOSOMES - 1)
        child1[0:split] = copy.copy(child2[0:split])  # [item1[::split],item2[split::]]
        child2[split:self.__N_CHROMOSOMES] = copy.copy(
            item1[split:self.__N_CHROMOSOMES])  # [item2[::split],item1[split::]]
        if self.__CAN_REPETEAD_CHRO is False:
            return self.__Replace_repeated(child1, child2, split)
        else:
            return [child1,child2]

    """
        Generate a child by mean method
    """

    def __Generate_Child_Mean(self, item1, item2):
        child = copy.copy(item1)
        if self.__CHRO_IS_F is True:
            for i in range(self.__N_CHROMOSOMES):
                child[i] = (item1[i]+item2[1])/2
        else:
            for i in range(self.__N_CHROMOSOMES):
                f = (item1[i] + item2[i])/2
                child[i] = int(math.floor(f))
        if self.__CAN_REPETEAD_CHRO is False:
            n=self.__CHRO_MINVALUE
            for i in range(self.__N_CHROMOSOMES):
                if child[i] in child [i+1:]:
                    while(True):
                        if n not in child:
                            child[i]=n
                            break
                        n+=1
        return child

    """
        Function that replace the chromosomes repeated
    """

    def __Replace_repeated(self, child1, child2, split):
        for i in range(0, split):
            if child1[i] in child1[split:self.__N_CHROMOSOMES]:
                for j in range(0, split):
                    if child2[j] in child2[split:self.__N_CHROMOSOMES]:
                        c1 = child1[i]
                        child1[i] = child2[j]
                        child2[j] = c1
                        break
        return [child1, child2]

    """
        Generate child main
    """

    def __Generate_Child(self, item1, item2 = None):
        if self.__TYPECHILD is CHILD_FLIP:
            return self.__Generate_Child_flip(item1)
        elif self.__TYPECHILD is CHILD_FLIP2:
            return self.__Generate_Child_tournament_Det(item1)
        elif self.__TYPECHILD is CHILD_SPLIT:
            return self.__Generate_Child_split(item1, item2)
        elif self.__TYPECHILD is CHILD_MEAN:
            return self.__Generate_Child_Mean(item1, item2)

    """
        Function that fill the pool
    """

    def __Fill_Next_Generation(self):
        new_pull = copy.copy(self.__POOL)
        if self.__TYPECHILD in [CHILD_FLIP, CHILD_FLIP2, CHILD_MEAN]:
            for i in (range(0, self.__rangechild)):
                child = self.__Generate_Child(copy.copy(self.__POOL[i][0]), item2 = self.__POOL[i+1][0])
                dest = i + self.__sizeelitism
                if randint(0, 99) < self.__MUTE:
                    child = self.__mute_individuals(child)
                new_pull[dest][0] = copy.copy(child)
        elif self.__TYPECHILD in [CHILD_SPLIT]:
            for i in (range(0, self.__rangechild, 2)):
                childs = self.__Generate_Child(copy.copy(self.__POOL[i][0]), item2 = copy.copy(self.__POOL[i + 1][0]))
                dest = i + self.__sizeelitism
                for j in [0,1]:
                    if randint(0, 99) < self.__MUTE:
                        childs[j] = self.__mute_individuals(childs[j])
                    new_pull[dest+j][0] = copy.copy(childs[j])
        return new_pull

    """
        Function that select the best item from a list of items for tournament selection.
    """

    def __Tournament_Selection_Deterministic(self, listItems):

        dict = {}
        for i in range(0, len(listItems)):
            dict[i] = self.__FUN_FITNESS(listItems[i])
        return listItems[sorted(dict, reverse = True)[0]]

    """
        Function that select the best item from a list of items for tournament selection.
    """

    def __Tournament_Selection_Probabilistic(self, listItems):
        return listItems[randint(0, len(listItems) - 1)]

    """
        Function that selct the individuos to fill next pool
    """

    def __Roulette(self):
        new_pool = copy.copy(self.__POOL)
        for i in (range(1, self.__SIZE_POOL)):
            self.__POOL[i][1] = self.__POOL[i][1] + self.__POOL[i - 1][1]
        for i in (range(0, self.__SIZE_POOL)):
            self.__POOL[i][2] = 1 - (self.__POOL[i][1] / self.__POOL[self.__SIZE_POOL - 1][1])

        if self.__TYPECHILD in [CHILD_FLIP, CHILD_FLIP2, CHILD_MEAN]:
            for i in (range(0, self.__rangechild)):
                selec = random()
                for j in range(0, self.__SIZE_POOL)[::-1]:
                    if selec < self.__POOL[j][2]:
                        break
                child = self.__Generate_Child(copy.copy(self.__POOL[j][0]),copy.copy(self.__POOL[j+1][0]))
                dest = i + self.__sizeelitism
                if randint(0, 99) < self.__MUTE:
                    child = self.__mute_individuals(child)
                new_pool[dest][0] = copy.copy(child)
        elif self.__TYPECHILD in [CHILD_SPLIT]:
            for i in (range(0, self.__rangechild, 2)):
                selec1 = random()
                selec2 = random()
                for j in range(0, self.__SIZE_POOL)[::-1]:
                    if selec1 < self.__POOL[j][2]:
                        break
                for k in range(0, self.__SIZE_POOL)[::-1]:
                    if selec2 < self.__POOL[k][2]:
                        break
                childs = self.__Generate_Child(copy.copy(self.__POOL[j][0]), copy.copy(self.__POOL[k][0]))
                dest = i + self.__sizeelitism
                for j in [0,1]:
                    if randint(0, 99) < self.__MUTE:
                        childs[j] = self.__mute_individuals(childs[j])
                    new_pool[dest+j][0] = copy.copy(childs[j])
        return new_pool

    """
        Function main for fill next pool, this call the different forms the generate next pool
    """

    def __Next_Generation(self):
        if self.__SELECTION_TYPE is FILL_NEXT_GENERATION:
            self.__Fill_Next_Generation()
        elif self.__SELECTION_TYPE is ROULETTE:
            self.__Roulette()

    """
        Function that mute a individuos
    """

    def __mute_individuals(self, item):
        index = [randint(0, self.__N_CHROMOSOMES - 1), randint(0, self.__N_CHROMOSOMES - 1)]
        index.sort()
        a = copy.copy(item[index[0]:index[1]])
        b = copy.copy(item)
        b[index[0]:index[1]] = copy.copy(sample(a, index[1] - index[0]))
        return b

    """
    def __mute_individuals_simple(self, item):
        return sample(item, self.__N_CHROMOSOMES)
    """

    """
        Asign a predefined pool and activate testing mode
    """

    def set_pool(self, pool):
        self.__TEST_POOL = True
        self.__POOL = copy.copy(pool)

    """
        Get a empty pool
    """

    def get_empty_pool(self):
        pool = [[[0 for x in range(self.__N_CHROMOSOMES)], 0, 0] for y in range(self.__SIZE_POOL)]
        return pool

    """
        Get the pool
    """

    def get_pool(self):
        return copy.copy(self.__POOL)

    """
        Print the individuals of the pool
    """
    def print_individuals(self):
        for i in range(0, self.__SIZE_POOL):
            print self.__POOL[i][:], ","

    """
        Return the win individual
    """

    def Winner_Probability(self):
        return self.__POOL[0][:]

    """
        Function main that run the algorithm
    """


    def run(self, print_best=0):
        for x in range(self.__ITMAX):
            for i in range(self.__SIZE_POOL):
                item = self.__Get_Individuos(i)
                self.__Set_Fittnes(i, self.__FUN_FITNESS(item))
            self.__sort_pool(self.__REVERSE)
            print "\rThe winer is: ", self.Winner_Probability()[1],
            if print_best is not 0:
                print "\rThe winer is: ", self.Winner_Probability()[1]
                for x in range(0, print_best):
                    print self.__POOL[x][0]
                sleep(1)
                print ("\n" * 100)
            else:
                print "\rThe winer is: ", self.Winner_Probability()[1],
            self.__Next_Generation()

        print "\rThe winer is: ", self.Winner_Probability()

    @QtCore.Slot()
    def __run(self):
        for i in range(self.__SIZE_POOL):
            item = self.__Get_Individuos(i)
            self.__Set_Fittnes(i, self.__FUN_FITNESS(item))
        self.__sort_pool(self.__REVERSE)
        print "\rThe winer is: ", self.Winner_Probability()[1],
        self.__Next_Generation()
    def help(self):
        s = """GeneticAlgorithm
        The structure of a tuple of the PULL is:
        [individual, FITNNES, PROBABILITY FOR THE ROULETTE]

        The structure of a individual is:
        [value,value,value,...,value] It has as many values as chromosomes.

        Ways to Generate Children:

            CHILD_FLIP
                father[1, 6, 7, 2, 6, 8, 2, 1, 5, 6, 3, 8, 7]
                                  [    father   ]
                child [1, 6, 7, 2, 5, 1, 2, 8, 6 ,6 ,3, 8, 7]
                                  [   r_father  ]
            CHILD_SPLIT
                father1[1, 6, 7, 2, 6, 8, 2, 1, 5, 6, 3, 8, 7]
                       [   father1_1    ][     father1_2     ]
                father1[5, 4, 8, 6, 3, 2, 8, 6, 5, 7, 9, 3, 7]
                       [   father2_1    ][     father2_2     ]
                child1 [1, 6, 7, 2, 6, 8, 8, 6, 5, 7, 9, 3, 7]
                       [   father1_1    ][     father2_2     ]
                child2 [5, 4, 8, 6, 3, 2, 2, 1, 5, 6, 3, 8, 7]
                       [   father2_1    ][     father1_2     ]

            CHILD_FLIP2
                father[1, 6, 7, 2, 6, 8, 2, 1, 5, 6, 3, 8, 7]
                      [ father_1 ][   father_2  ][ father_3 ]
                child1[1, 6, 7, 2, 5, 1, 2, 8, 6 ,6 ,3, 8, 7]
                      [ father_1 ][  r_father_2 ][ father_3 ]
                child2[2, 7, 6, 1, 6, 8, 2, 1, 5, 7, 8, 3, 6]
                      [r_father_1][   father_2  ][r_father_3]
                return the best [father, child1, child2]

            CHILD_MEAN and chromosomes_is_float = True
                father1 [1, 5, 7, 6]
                father2 [3, 8, 1, 3]
                child   [2, 6.5, 4, 4.5]  child[i] = (father1[i]+father2[i])/2

            CHILD_MEAN and chromosomes_is_float = False
                father1 [1, 5, 7, 6]
                father2 [3, 8, 1, 3]
                child   [2, 6, 4, 4]  child[i] = floor((father1[i]+father2[i])/2)

        Example:
        This is the typical travelling salesman problem (TSP) in this case there are 20 cities.

from Genetic_Algorithm import *


ELITISM = 10
MUTE = 2
REVERSE = True
SELECTION_TYPE = FILL_NEXT_GENERATION
SIZE_PULL = 1000
N_CHROMOSOMES = 20
HIGH_LOW = False
ITMAX = 100
TYPECHILD = CHILD_FLIP
distance = [[9.22337203685e+18, 77.0, 30.0, 52.0, 30.0, 28.0, 28.0, 91.0, 35.0, 26.0, 61.0, 56.0, 27.0, 44.0, 35.0, 71.0, 55.0, 58.0, 30.0, 74.0] ,
            [77.0, 9.22337203685e+18, 41.0, 39.0, 82.0, 64.0, 72.0, 99.0, 89.0, 28.0, 40.0, 64.0, 72.0, 86.0, 86.0, 82.0, 94.0, 33.0, 64.0, 42.0] ,
            [30.0, 41.0, 9.22337203685e+18, 22.0, 37.0, 32.0, 39.0, 22.0, 83.0, 41.0, 92.0, 77.0, 88.0, 46.0, 55.0, 28.0, 23.0, 56.0, 21.0, 60.0] ,
            [52.0, 39.0, 22.0, 9.22337203685e+18, 49.0, 55.0, 90.0, 94.0, 24.0, 22.0, 74.0, 26.0, 72.0, 26.0, 36.0, 93.0, 61.0, 98.0, 69.0, 49.0] ,
            [30.0, 82.0, 37.0, 49.0, 9.22337203685e+18, 30.0, 61.0, 55.0, 65.0, 26.0, 23.0, 73.0, 77.0, 99.0, 35.0, 82.0, 41.0, 90.0, 93.0, 60.0] ,
            [28.0, 64.0, 32.0, 55.0, 30.0, 9.22337203685e+18, 42.0, 83.0, 39.0, 36.0, 24.0, 95.0, 55.0, 98.0, 20.0, 58.0, 92.0, 95.0, 91.0, 30.0] ,
            [28.0, 72.0, 39.0, 90.0, 61.0, 42.0, 9.22337203685e+18, 61.0, 54.0, 28.0, 91.0, 77.0, 55.0, 62.0, 96.0, 31.0, 23.0, 91.0, 49.0, 100.0] ,
            [91.0, 99.0, 22.0, 94.0, 55.0, 83.0, 61.0, 9.22337203685e+18, 43.0, 100.0, 46.0, 65.0, 90.0, 60.0, 63.0, 80.0, 69.0, 39.0, 60.0, 62.0] ,
            [35.0, 89.0, 83.0, 24.0, 65.0, 39.0, 54.0, 43.0, 9.22337203685e+18, 31.0, 97.0, 56.0, 93.0, 94.0, 39.0, 33.0, 32.0, 46.0, 94.0, 92.0] ,
            [26.0, 28.0, 41.0, 22.0, 26.0, 36.0, 28.0, 100.0, 31.0, 9.22337203685e+18, 70.0, 81.0, 22.0, 43.0, 21.0, 72.0, 99.0, 70.0, 38.0, 98.0] ,
            [61.0, 40.0, 92.0, 74.0, 23.0, 24.0, 91.0, 46.0, 97.0, 70.0, 9.22337203685e+18, 73.0, 69.0, 59.0, 71.0, 64.0, 78.0, 66.0, 42.0, 80.0] ,
            [56.0, 64.0, 77.0, 26.0, 73.0, 95.0, 77.0, 65.0, 56.0, 81.0, 73.0, 9.22337203685e+18, 73.0, 28.0, 36.0, 91.0, 64.0, 68.0, 30.0, 26.0] ,
            [27.0, 72.0, 88.0, 72.0, 77.0, 55.0, 55.0, 90.0, 93.0, 22.0, 69.0, 73.0, 9.22337203685e+18, 79.0, 73.0, 43.0, 87.0, 65.0, 30.0, 27.0] ,
            [44.0, 86.0, 46.0, 26.0, 99.0, 98.0, 62.0, 60.0, 94.0, 43.0, 59.0, 28.0, 79.0, 9.22337203685e+18, 88.0, 40.0, 39.0, 68.0, 31.0, 70.0] ,
            [35.0, 86.0, 55.0, 36.0, 35.0, 20.0, 96.0, 63.0, 39.0, 21.0, 71.0, 36.0, 73.0, 88.0, 9.22337203685e+18, 54.0, 58.0, 50.0, 29.0, 63.0] ,
            [71.0, 82.0, 28.0, 93.0, 82.0, 58.0, 31.0, 80.0, 33.0, 72.0, 64.0, 91.0, 43.0, 40.0, 54.0, 9.22337203685e+18, 39.0, 84.0, 49.0, 25.0] ,
            [55.0, 94.0, 23.0, 61.0, 41.0, 92.0, 23.0, 69.0, 32.0, 99.0, 78.0, 64.0, 87.0, 39.0, 58.0, 39.0, 9.22337203685e+18, 68.0, 63.0, 60.0] ,
            [58.0, 33.0, 56.0, 98.0, 90.0, 95.0, 91.0, 39.0, 46.0, 70.0, 66.0, 68.0, 65.0, 68.0, 50.0, 84.0, 68.0, 9.22337203685e+18, 79.0, 87.0] ,
            [30.0, 64.0, 21.0, 69.0, 93.0, 91.0, 49.0, 60.0, 94.0, 38.0, 42.0, 30.0, 30.0, 31.0, 29.0, 49.0, 63.0, 79.0, 9.22337203685e+18, 26.0] ,
            [74.0, 42.0, 60.0, 49.0, 60.0, 30.0, 100.0, 62.0, 92.0, 98.0, 80.0, 26.0, 27.0, 70.0, 63.0, 25.0, 60.0, 87.0, 26.0, 9.22337203685e+18]]
def fitnnes(item):
    dist = 0
    cityant = item[0]
    for cityact in item[1:N_CHROMOSOMES]:
        dist = dist + distance[cityant][cityact]
        cityant = cityact
    dist = dist + distance[cityant][item[0]]
    return dist

if __name__ ==  "__main__":
    print "["
    for x in distance:
        print x[:20], ","
    print "]"
    f = fitnnes
    chro = chromosome_t(N_CHROMOSOMES)
    try:
        GA = GeneticAlgorithm(f, chro, itmax = ITMAX, selection_type = SELECTION_TYPE,
                            High_Low = HIGH_LOW, size_pool = SIZE_PULL, child_type = TYPECHILD, porcent_elitism = ELITISM, porcent_mute = MUTE)
        GA.run()
    except GenecticException:
        print GenecticException.what


        """
        print s
