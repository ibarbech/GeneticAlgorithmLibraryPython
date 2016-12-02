from __builtin__ import str

from random import *
import copy

ROULETTE = 1
FILL_NEXT_GENERATION = 2

CHILD_FLIP = 10


class B(Exception):
    pass


class GenecticException(B):
    what = None


class GeneticAlgorithm:
    def __init__(self, n_chromosomes, fun_fitness, itmax=50, child_type=CHILD_FLIP, selection_type=FILL_NEXT_GENERATION,
                 High_Low=False, size_pool=1000, porcent_elitism=10, porcent_mute=2, testing=False):

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
        self.__N_CHROMOSOMES = n_chromosomes
        self.__POOL = self.__Generate_pool()
        self.__FUN_FITNESS = fun_fitness
        self.__ITMAX = itmax
        self.__TYPECHILD = child_type
        self.__rangechild = (int)(self.__SIZE_POOL - self.__SIZE_POOL * self.__ELITISM)
        self.__sizeelitism = (int)(self.__SIZE_POOL * self.__ELITISM)
        self.__TEST_POOL = testing  # Flag for testing purpose

    def __Generate_pool(self):
        new_pool = [[[0 for x in range(self.__N_CHROMOSOMES)], 0, 0] for y in range(self.__SIZE_POOL)]
        for i in range(0, self.__SIZE_POOL):
            new_pool[i][0] = sample(range(self.__N_CHROMOSOMES), self.__N_CHROMOSOMES)
        return new_pool

    def __getKey(self, item):
        return item[1]

    def __Get_Individuos(self, individual):
        if individual not in range(0, self.__SIZE_POOL):
            a = GenecticException
            a.what = "Error: individual", individual, " not existing, 0 <= individual < " + str(self.__SIZE_POOL)
            raise a
        return copy.copy(self.__POOL[individual][0])

    def __Set_Fittnes(self, individual, Fittnes):
        if individual not in range(0, self.__SIZE_POOL):
            a = GenecticException
            a.what = "Error: individual", individual, " not existing, 0 <= individual < " + str(self.__SIZE_POOL)
            raise a
        self.__POOL[individual][1] = Fittnes

    def __sort_pool(self, rever=False):
        self.__POOL.sort(key=self.__getKey, reverse=rever)

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

    def __Generate_Child(self, item):
        if self.__TYPECHILD is CHILD_FLIP:
            return self.__Generate_Child_flip(item)

    def __Fill_Next_Generation(self):
        new_pool = copy.copy(self.__POOL)
        for i in (range(0, self.__rangechild)):
            child = self.__Generate_Child(copy.copy(self.__POOL[i][0]))
            dest = i + self.__sizeelitism
            if randint(0, 99) < self.__MUTE:
                child = self.__mute_individuals(child)
            new_pool[dest][0] = copy.copy(child)
        return new_pool

    """
        Function that select the best item from a list of items for tournament selection.
    """

    def __Tournament_Selection_Deterministic(self, listItems):

        dict = {}
        for i in range(0, len(listItems)):
            dict[i] = self.__FUN_FITNESS(listItems[i])
        return listItems[sorted(dict, reverse=True)[0]]

    """
        Function that select the best item from a list of items for tournament selection.
    """

    def __Tournament_Selection_Probabilistic(self, listItems):
        return listItems[randint(0, len(listItems) - 1)]

    """
        Asign a predefined pool and activate testing mode
    """

    def setPool(self, new_Pool):
        self.__TEST_POOL = True
        for i in range(0, self.__SIZE_POOL):
            self.__POOL[i][0] = copy.copy(new_Pool[i])

    def __Roulette(self):
        None

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

    def __mute_individuals_simple(self, item):
        return sample(item, self.__N_CHROMOSOMES)

    def print_individuals(self):
        for i in range(0, self.__SIZE_POOL):
            print self.__POOL[i][:], ","

    def Winner_Probability(self):
        return self.__POOL[0][:]

    def run(self):
        for x in range(self.__ITMAX):
            self.__Next_Generation()
            for i in range(self.__SIZE_POOL):
                item = self.__Get_Individuos(i)
                self.__Set_Fittnes(i, self.__FUN_FITNESS(item))
            self.__sort_pool(self.__REVERSE)
            print "\rThe winer is: ", self.Winner_Probability()[1],

        print "\rThe winer is: ", self.Winner_Probability()
