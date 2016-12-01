from __builtin__ import str

import cv2
import numpy
from random import *
import copy
import sys
from time import *


ROULETTE = 1
FILL_NEXT_GENERATION = 2

CHILD_FLIP=10

class B(Exception):
    pass

class GenecticException(B):
    what = None

class GeneticAlgorithm:


    def __init__(self, n_chromosomes,fun_fitness, itmax=50, child_type=CHILD_FLIP, selection_type=FILL_NEXT_GENERATION,
                 High_Low=False, size_pull=1000, porcent_elitism=10, porcent_mute = 2):

        if selection_type not in [ROULETTE, FILL_NEXT_GENERATION]:
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
        self.__TYPECHILD=child_type
        self.__rangechild=(int)(self.__SIZE_PULL - self.__SIZE_PULL * self.__ELITISM)
        self.__sizeelitism=(int)(self.__SIZE_PULL * self.__ELITISM)

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

    def __Generate_Child_flip(self, item):
        child = copy.copy(item)
        index = [randint(0, self.__N_CHROMOSOMES - 1), randint(0, self.__N_CHROMOSOMES - 1)]
        index.sort()
        revert = copy.copy(item[index[0]:index[1]])
        child[index[0]:index[1]] = revert[::-1]
        return child

    def __Generate_Child(self, item):
        if self.__TYPECHILD is CHILD_FLIP:
            return self.__Generate_Child_flip(item)

    def __Fill_Next_Generation(self):
        new_pull=copy.copy(self.__pull)
        for i in (range(0, self.__rangechild)):
            child = self.__Generate_Child(copy.copy(self.__pull[i][0]))
            dest = i + self.__sizeelitism
            if randint(0, 99) < self.__MUTE:
                child = self.__mute_individuals(child)
            new_pull[dest][0] = copy.copy(child)
        return new_pull

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
        for i in range(0, self.__SIZE_PULL):
            print self.__pull[i][:], ","

    def Winner_Probability(self):
        return self.__pull[0][:]

    def run(self):
        self.__Next_Generation()
        for x in range(self.__ITMAX):
            self.__Next_Generation()
            print "\rThe winer is: ", self.Winner_Probability()[1],
            for i in range(self.__SIZE_PULL):
                item=self.__Get_Individuos(i)
                self.__Set_Fittnes(i, self.__FUN_FITNESS(item))
            self.__sort_pull(self.__REVERSE)

        print "\rThe winer is: ",self.Winner_Probability()



