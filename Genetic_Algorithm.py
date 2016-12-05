from __builtin__ import str

from random import *
import copy
from time import *

ROULETTE = 1
FILL_NEXT_GENERATION = 2

CHILD_FLIP = 10
CHILD_SPLIT = 11
CHILD_FLIP2 = 12




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

    def __getKey(self, item):
        return item[1]

    def __Get_Individuos(self, individual):
        if individual not in range(0, self.__SIZE_POOL):
            a = GenecticException
            a.what = "Error: individual", individual, " not existing, 0 < = individual < " + str(self.__SIZE_POOL)
            raise a
        return copy.copy(self.__POOL[individual][0])

    def __Set_Fittnes(self, individual, Fittnes):
        if individual not in range(0, self.__SIZE_POOL):
            a = GenecticException
            a.what = "Error: individual", individual, " not existing, 0 < = individual < " + str(self.__SIZE_POOL)
            raise a
        self.__POOL[individual][1] = Fittnes

    def __sort_pool(self, rever = False):
        self.__POOL.sort(key = self.__getKey, reverse = rever)

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

    def __Generate_Child(self, item1, item2 = None):
        if self.__TYPECHILD is CHILD_FLIP:
            return self.__Generate_Child_flip(item1)
        elif self.__TYPECHILD is CHILD_FLIP2:
            return self.__Generate_Child_tournament_Det(item1)
        elif self.__TYPECHILD is CHILD_SPLIT:
            return self.__Generate_Child_split(item1, item2)

    def __Fill_Next_Generation(self):
        new_pull = copy.copy(self.__POOL)
        if self.__TYPECHILD in [CHILD_FLIP,CHILD_FLIP2]:
            for i in (range(0, self.__rangechild)):
                child = self.__Generate_Child(copy.copy(self.__POOL[i][0]))
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

    def __Roulette(self):
        new_pool = copy.copy(self.__POOL)
        for i in (range(1, self.__SIZE_POOL)):
            self.__POOL[i][1] = self.__POOL[i][1] + self.__POOL[i - 1][1]
        for i in (range(0, self.__SIZE_POOL)):
            self.__POOL[i][2] = 1 - (self.__POOL[i][1] / self.__POOL[self.__SIZE_POOL - 1][1])

        if self.__TYPECHILD in [CHILD_FLIP,CHILD_FLIP2]:
            for i in (range(0, self.__rangechild)):
                selec = random()
                for j in range(0, self.__SIZE_POOL)[::-1]:
                    if selec < self.__POOL[j][2]:
                        break
                child = self.__Generate_Child(copy.copy(self.__POOL[j][0]))
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

    def __Next_Generation(self):
        if self.__SELECTION_TYPE is FILL_NEXT_GENERATION:
            self.__Fill_Next_Generation()
        elif self.__SELECTION_TYPE is ROULETTE:
            self.__Roulette()

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

    def get_empty_pool(self):
        pool = [[[0 for x in range(self.__N_CHROMOSOMES)], 0, 0] for y in range(self.__SIZE_POOL)]
        return pool

    def get_pool(self):
        return copy.copy(self.__POOL)

    def print_individuals(self):
        for i in range(0, self.__SIZE_POOL):
            print self.__POOL[i][:], ","

    def Winner_Probability(self):
        return self.__POOL[0][:]

    def run(self, print_best = 0):
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
        """
        print s
