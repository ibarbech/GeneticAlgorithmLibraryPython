from __builtin__ import str

import cv2
import numpy
from random import *
import copy
import sys
from time import *


SELECTION_ROULETTE = 1
SELECTION_TOURNAMENT = 2

class B(Exception):
    pass

class GenecticException(B):
    what = None
    pass

class GeneticAlgorithm:


    def __init__(self, n_chromosomes, itmax=50,fun_fitness=None ,selection_type=SELECTION_TOURNAMENT,High_Low=False, size_pull=1000, porcent_elitism=10, porcent_mute = 2):

        if selection_type not in [SELECTION_ROULETTE,SELECTION_TOURNAMENT]:
            a = GenecticException
            a.what = "Error: selection_type is not correct."
            raise a
            exit(-1)
        if porcent_elitism not in range(100):
            a = GenecticException
            a.what = "Error: porcent_elitism not in range [0,100]"
            raise a
            exit(-1)
        if porcent_mute not in range(100):
            a = GenecticException
            a.what = "Error: porcent_mute not in range [0,100]"
            raise a
            exit(-1)
        if High_Low not in [True,False]:
            a = GenecticException
            a.what = "Error: High_Low must be True or False","Error: fun_fitness is None"
            raise a
            exit(-1)
        self.__ELITISM = porcent_elitism / 100.0
        self.__MUTE = porcent_mute
        self.__REVERSE = High_Low
        self.__SELECTION_TYPE = selection_type
        self.__SIZE_PULL = size_pull
        self.__N_CHROMOSOMES = n_chromosomes
        self.__pull=self.__Generate_pull()
        self.__FUN_FITNESS=fun_fitness
        self.__ITMAX=itmax

    def __Generate_pull(self):
        new_pull = [[[0 for x in range(self.__N_CHROMOSOMES)], 0, 0] for y in range(self.__SIZE_PULL)]
        for i in range(0, self.__SIZE_PULL):
            new_pull[i][0] = sample(range(self.__N_CHROMOSOMES), self.__N_CHROMOSOMES)
        return new_pull

    def __getKey(self, item):
        return item[1]

    def __Get_Individuos(self, individual):
        if individual not in range(0, self.__SIZE_PULL):
            a = GenecticException
            a.what = "Error: individual",individual," not existing, 0 <= individual < " + str(self.__SIZE_PULL)
            raise a
            return -1
        return copy.copy(self.__pull[individual][0])

    def __Set_Fittnes(self, individual, Fittnes):
        if individual not in range(0, self.__SIZE_PULL):
            a = GenecticException
            a.what = "Error: individual",individual," not existing, 0 <= individual < " + str(self.__SIZE_PULL)
            raise a
            exit(-1)
        self.__pull[individual][1]=Fittnes

    def __sort_pull(self, rever=False):
        self.__pull.sort(key=self.__getKey, reverse=rever)

    def __Next_Generation_Tournamet(self):
        new_pull=copy.copy(self.__pull)
        for i in (range(0, int(self.__SIZE_PULL - self.__SIZE_PULL * self.__ELITISM))):
            child = copy.copy(self.__pull[i][0])
            dest = i + int(self.__SIZE_PULL * self.__ELITISM)
            if randint(0, 99) < self.__MUTE:
                child = self.__mute_individuals(child)
            else:
                index = [randint(0, self.__N_CHROMOSOMES - 1), randint(0, self.__N_CHROMOSOMES - 1)]
                index.sort()
                revert = copy.copy(child[index[0]:index[1]])
                child[index[0]:index[1]] = copy.copy(revert[::-1])
            new_pull[dest][0] = copy.copy(child)
        return new_pull

    def __Next_Generation_ROULETE(self):
        None

    def __Next_Generation(self):
        if self.__SELECTION_TYPE is SELECTION_TOURNAMENT:
            self.__Next_Generation_Tournamet()
        elif self.__SELECTION_TYPE is SELECTION_ROULETTE:
            None

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
        for i in range(0, self.__SIZE_PULL):
            print self.__pull[i][:], ","

    def Winner_Probability(self):
        return self.__pull[0][:]

    def run(self):
        if self.__FUN_FITNESS is not None:
            for x in range(self.__ITMAX):
                print "\rThe winer is: ", self.Winner_Probability()[1],
                for i in range(self.__SIZE_PULL):
                    item=self.__Get_Individuos(i)
                    self.__Set_Fittnes(i, self.__FUN_FITNESS(item))
                self.__sort_pull(self.__REVERSE)
                self.__Next_Generation()
            print "\rThe winer is: ",self.Winner_Probability()
        else:
            a = GenecticException
            a.what = "Error: fun_Fitnes is None"
            raise a
            exit(-1)
            return -1



