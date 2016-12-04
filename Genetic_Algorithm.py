from __builtin__ import str

from random import *
import copy

ROULETTE = 1
FILL_NEXT_GENERATION = 2

CHILD_FLIP = 10
CHILD_SPLIT = 11

class B(Exception):
    pass


class GenecticException(B):
    what = None

class chormosoma_t():
    def __init__(self,n_chromosomes,maxvalue = None,minvalue = 0,chromosomes_is_float = False,):
        self.N_CHRO = n_chromosomes
        if maxvalue is None:
            self.MAXVALUE = n_chromosomes
        else:
            self.MAXVALUE = maxvalue
        self.MINVALUE = minvalue
        self.CHRO_IS_F = chromosomes_is_float

class GeneticAlgorithm:


    def __init__(self,fun_fitness, chromosomes, itmax = 50, child_type = CHILD_FLIP, selection_type = FILL_NEXT_GENERATION,
                 High_Low = False, size_pull = 1000, porcent_elitism = 10, porcent_mute = 2, testing=False):

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
        self.__SIZE_PULL = size_pull
        self.__N_CHROMOSOMES = chromosomes.N_CHRO
        self.__FUN_FITNESS = fun_fitness
        self.__ITMAX = itmax
        self.__TYPECHILD = child_type
        self.__rangechild = (int)(self.__SIZE_PULL - self.__SIZE_PULL * self.__ELITISM)
        self.__sizeelitism = (int)(self.__SIZE_PULL * self.__ELITISM)
        self.__CHRO_IS_F = chromosomes.CHRO_IS_F
        self.__CHRO_MAXVALUE = chromosomes.MAXVALUE
        self.__CHRO_MINVALUE = chromosomes.MINVALUE
        self.__pull = self.__Generate_pull()
        self.__TEST_POOL = testing  # Flag for testing purpose

        
    def __Generate_pull(self):
        if self.__CHRO_IS_F is False:
            ind = range(self.__CHRO_MINVALUE, self.__CHRO_MAXVALUE)
            new_pull = [[sample(ind,self.__N_CHROMOSOMES), 0, 0] for y in range(self.__SIZE_PULL)]
            return new_pull
        else:
            new_pull = [[[uniform(self.__CHRO_MINVALUE,self.__CHRO_MAXVALUE) for x in range(self.__N_CHROMOSOMES)], 0, 0] for y in range(self.__SIZE_PULL)]
            return new_pull

    def __getKey(self, item):
        return item[1]

    def __Get_Individuos(self, individual):
        if individual not in range(0, self.__SIZE_POOL):
            a = GenecticException
            a.what = "Error: individual",individual," not existing, 0 < = individual < " + str(self.__SIZE_PULL)
            raise a
        return copy.copy(self.__pull[individual][0])

    def __Set_Fittnes(self, individual, Fittnes):
        if individual not in range(0, self.__SIZE_PULL):
            a = GenecticException
            a.what = "Error: individual",individual," not existing, 0 < = individual < " + str(self.__SIZE_PULL)
            raise a
        self.__pull[individual][1] = Fittnes

    def __sort_pull(self, rever = False):
        self.__pull.sort(key = self.__getKey, reverse = rever)

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


    def __Generate_Child_split(self, item1,item2):
        child1 = copy.copy(item1)
        child2 = copy.copy(item2)
        split = randint(1, self.__N_CHROMOSOMES - 1)
        child1[0:split] = copy.copy(child2[0:split])                          #[item1[::split],item2[split::]]
        child2[split:self.__N_CHROMOSOMES] = copy.copy(item1[split:self.__N_CHROMOSOMES])         #[item2[::split],item1[split::]]
        return self.__Replace_repeated(child1,child2,split)

    def __Replace_repeated(self,child1,child2,split):
        for i in range(0, split):
            if child1[i] in child1[split:self.__N_CHROMOSOMES]:
                for j in range(0, split):
                    if child2[j] in child2[split:self.__N_CHROMOSOMES]:
                        c1 = child1[i]
                        child1[i] = child2[j]
                        child2[j] = c1
                        break
        return [child1,child2]

    def __Generate_Child(self, item1,item2 = None):
        if self.__TYPECHILD is CHILD_FLIP:
            return self.__Generate_Child_flip(item1)
        elif self.__TYPECHILD is CHILD_SPLIT:
            return self.__Generate_Child_split(item1,item2)

    def __Fill_Next_Generation(self):
        new_pull = copy.copy(self.__pull)
        if self.__TYPECHILD is CHILD_FLIP:
            for i in (range(0, self.__rangechild)):
                child = self.__Generate_Child(copy.copy(self.__pull[i][0]))
                dest = i + self.__sizeelitism
                if randint(0, 99) < self.__MUTE:
                    child = self.__mute_individuals(child)
                new_pull[dest][0] = copy.copy(child)
        elif self.__TYPECHILD is CHILD_SPLIT:
            for i in (range(0, self.__rangechild,2)):
                childs = self.__Generate_Child(copy.copy(self.__pull[i][0]),item2 = copy.copy(self.__pull[i+1][0]))
                dest1 = i + self.__sizeelitism
                dest2 = dest1+1
                if randint(0, 99) < self.__MUTE:
                    childs[0] = self.__mute_individuals(childs[0])
                if randint(0, 99) < self.__MUTE:
                    childs[1] = self.__mute_individuals(childs[1])
                new_pull[dest1][0] = copy.copy(childs[0])
                new_pull[dest2][0] = copy.copy(childs[1])
        return new_pull

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
        new_pull = copy.copy(self.__pull)
        for i in (range(1, self.__SIZE_PULL)):
            self.__pull[i][1] = self.__pull[i][1]+self.__pull[i-1][1]
        for i in (range(0, self.__SIZE_PULL)):
            self.__pull[i][2] = 1 - (self.__pull[i][1]/self.__pull[self.__SIZE_PULL-1][1])

        if self.__TYPECHILD is CHILD_FLIP:
            for i in (range(0, self.__rangechild)):
                selec = random()
                for j in range(0,self.__SIZE_PULL)[::-1]:
                    if selec <self.__pull[j][2]:
                        break
                child = self.__Generate_Child(copy.copy(self.__pull[j][0]))
                dest = i + self.__sizeelitism
                if randint(0, 99) < self.__MUTE:
                    child = self.__mute_individuals(child)
                new_pull[dest][0] = copy.copy(child)
        elif self.__TYPECHILD is CHILD_SPLIT:
            for i in (range(0, self.__rangechild,2)):
                selec1 = random()
                selec2 = random()
                for j in range(0, self.__SIZE_PULL)[::-1]:
                    if selec1 < self.__pull[j][2]:
                        break
                for k in range(0, self.__SIZE_PULL)[::-1]:
                    if selec2 < self.__pull[k][2]:
                        break
                childs = self.__Generate_Child(copy.copy(self.__pull[j][0]),copy.copy(self.__pull[k][0]))
                dest1 = i + self.__sizeelitism
                dest2 = dest1+1
                if randint(0, 99) < self.__MUTE:
                    childs[0] = self.__mute_individuals(childs[0])
                if randint(0, 99) < self.__MUTE:
                    childs[1] = self.__mute_individuals(childs[1])
                new_pull[dest1][0] = copy.copy(childs[0])
                new_pull[dest2][0] = copy.copy(childs[1])
        return new_pull

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

	# TODO - DEPRECATED
    def set_pull(self, pull):
        self.__pull = copy.copy(pull)

    def get_empty_pull(self):
        pull = [[[0 for x in range(self.__N_CHROMOSOMES)], 0, 0] for y in range(self.__SIZE_PULL)]
        return pull

    def get_pull(self):
        return copy.copy(self.__pull)

    def print_individuals(self):
        for i in range(0, self.__SIZE_PULL):
            print self.__pull[i][:], ","

    def Winner_Probability(self):
        return self.__pull[0][:]

    def run(self,print_best=0):
        for x in range(self.__ITMAX):
            for i in range(self.__SIZE_PULL):
                item = self.__Get_Individuos(i)
                self.__Set_Fittnes(i, self.__FUN_FITNESS(item))
            self.__sort_pull(self.__REVERSE)
            print "\rThe winer is: ", self.Winner_Probability()[1],
            if print_best is not 0:
                print "\rThe winer is: ", self.Winner_Probability()[1]
                for x in range(0,print_best):
                    print self.__pull[x][0]
                sleep(1)
                print ("\n" * 100)
            else :
                print "\rThe winer is: ", self.Winner_Probability()[1],
            self.__Next_Generation()


        print "\rThe winer is: ",self.Winner_Probability()

    def help(self):
        s = """GeneticAlgorithm
        The structure of a tuple of the PULL is:
        [individual, FITNNES, PROBABILITY FOR THE ROULETTE]

        The structure of a individual is:
        [value,value,value,...,value] It has as many values as chromosomes.




        """



