from __init__ import *

DEBUG = False

ROULETTE = 1
FILL_NEXT_GENERATION = 2

CHILD_FLIP = 10
CHILD_SPLIT = 11
CHILD_FLIP_TOURNAMENT_DETERMINISTIC = 12
CHILD_FLIP_TOURNAMENT_PROBABILISTIC = 13
CHILD_MEAN = 14
CHILD_SPLIT_TOURNAMENT_DETERMINISTIC = 15
CHILD_SPLIT_TOURNAMENT_PROBABILISTIC = 16

types_childs_1 = [CHILD_FLIP,CHILD_FLIP_TOURNAMENT_DETERMINISTIC,CHILD_FLIP_TOURNAMENT_PROBABILISTIC,CHILD_MEAN,
                  CHILD_SPLIT_TOURNAMENT_DETERMINISTIC,CHILD_SPLIT_TOURNAMENT_PROBABILISTIC]

types_childs_2 = [CHILD_SPLIT]

types_Child = [CHILD_FLIP,CHILD_SPLIT,CHILD_MEAN,CHILD_FLIP_TOURNAMENT_DETERMINISTIC,CHILD_FLIP_TOURNAMENT_PROBABILISTIC,
               CHILD_SPLIT_TOURNAMENT_DETERMINISTIC,CHILD_SPLIT_TOURNAMENT_PROBABILISTIC]

types_selection= [FILL_NEXT_GENERATION,ROULETTE]

class GenecticException(Exception):
    what = None


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

if inspect.stack()[0][3] ==  "__main__":
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

    def __init__(self):
        if DEBUG:
            print inspect.stack()[0][3]
        try:
            self.__attr = None
            self.__POOL = None
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.__run)
        except:
            raise

    def setattrGeneticAlgorithm(self, GA_attr):
        """
        Set the params to instance, this function can raise a GeneticException
        :param GA_attr: contains params for the instance
        """
        try:
            self.__attr=GA_attr
            self.__POOL=self.__Generate_pool()
        except:
            raise

    def getattrGemeticAlgorithm(self):
        """
        Function that return all params in a intance of class GeneticAlgorithm_Attr_t
        :return: self.__attr
        """
        return copy.copy(self.__attr)

    def __Generate_pool(self):
        """
            Function that generate a pool
        """
        if DEBUG:
            print inspect.stack()[0][3]
        if self.__attr.CHRO_IS_F is False:
            if self.__attr.CAN_REPETEAD_CHRO is False:
                ind = range(self.__attr.CHRO_MINVALUE, self.__attr.CHRO_MAXVALUE)
                new_pool = [[sample(ind, self.__attr.N_CHROMOSOMES), 0, 0] for y in range(self.__attr.SIZE_POOL)]
            else:
                new_pool = [[[randint(self.__attr.CHRO_MINVALUE,self.__attr.CHRO_MAXVALUE) for x in range(self.__attr.N_CHROMOSOMES)], 0, 0] for y in range(self.__attr.SIZE_POOL)]
            return new_pool
        else:
            new_pool = [
                [[uniform(self.__attr.CHRO_MINVALUE, self.__attr.CHRO_MAXVALUE) for x in range(self.__attr.N_CHROMOSOMES)], 0, 0] for y
                in range(self.__attr.SIZE_POOL)]
            return new_pool

    def __getKey(self, item):
        """
            Function that returns a key to sort pool
        """
        #if DEBUG:
        #    print inspect.stack()[0][3]
        return item[1]

    def __Get_Individuos(self, individual):
        """
            Function that returns a individuos i
        """
        #if DEBUG:
        #    print inspect.stack()[0][3]
        if individual not in range(0, self.__attr.SIZE_POOL):
            a = GenecticException
            a.what = "Error: individual", individual, " not existing, 0 < = individual < " + str(self.__attr.SIZE_POOL)
            raise a
        return copy.copy(self.__POOL[individual][0])

    def __Set_Fittnes(self, individual, Fittnes):
        """
            Function that set the Fittnes to sort pool
        """
        #if DEBUG:
        #    print inspect.stack()[0][3]
        if individual not in range(0, self.__attr.SIZE_POOL):
            a = GenecticException
            a.what = "Error: individual", individual, " not existing, 0 < = individual < " + str(self.__attr.SIZE_POOL)
            raise a
        self.__POOL[individual][1] = Fittnes

    def __sort_pool(self, rever = False):
        """
            Function that sort pool if rever is True sort of highest to lowest else lowest to highest
        """
        #if DEBUG:
        #    print inspect.stack()[0][3]
        self.__POOL.sort(key = self.__getKey, reverse = rever)

    def __Generate_Child_flip(self, item):
        """
            Generate a child by flip method
        """
        if DEBUG:
            print inspect.stack()[0][3]
        child = copy.copy(item)
        index = [randint(0, self.__attr.N_CHROMOSOMES - 1), randint(0, self.__attr.N_CHROMOSOMES - 1)]
        index.sort()
        revert = copy.copy(item[index[0]:index[1]])
        child[index[0]:index[1]] = revert[::-1]
        return child

    def __Generate_Child_Flip_tournament(self, item):
        """
            Generate two sons by flip method, after that it returns the best between Father and the two sons.
        """
        if DEBUG:
            print inspect.stack()[0][3]
        child = copy.copy(item)
        index = [randint(0, self.__attr.N_CHROMOSOMES - 1), randint(0, self.__attr.N_CHROMOSOMES - 1)]
        index.sort()
        revert = copy.copy(item[index[0]:index[1]])
        child[index[0]:index[1]] = revert[::-1]

        child2 = copy.copy(item)
        revert2left = child2[0:index[0]]
        revert2right = child2[index[1]: self.__attr.N_CHROMOSOMES - 1]
        child2[0:index[0]] = revert2left[::-1]
        child2[index[1]:self.__attr.N_CHROMOSOMES - 1] = revert2right[::-1]

        listIndividual = [item, child, child2]
        if self.__attr.TYPECHILD is CHILD_FLIP_TOURNAMENT_DETERMINISTIC:
            return self.__Tournament_Selection_Deterministic(listIndividual)
        elif self.__attr.TYPECHILD is CHILD_FLIP_TOURNAMENT_PROBABILISTIC:
            return self.__Tournament_Selection_Probabilistic(listIndividual)

    def __Generate_Child_split(self, item1, item2):
        """
            Generate two sons by split method
        """
        if DEBUG:
            print inspect.stack()[0][3]
        child1 = copy.copy(item1)
        child2 = copy.copy(item2)
        split = randint(1, self.__attr.N_CHROMOSOMES - 1)
        child1[split:] = copy.copy(child2[split:])  # [item1[::split],item2[split::]]
        child2[split:] = copy.copy(item1[split:])  # [item2[::split],item1[split::]]
        if self.__attr.CAN_REPETEAD_CHRO is False:
            return [self.__Replace_repeated(child1),self.__Replace_repeated(child2)]
        else:
            return [child1,child2]

    def __Generate_Child_Mean(self, item1, item2):
        """
            Generate a child by mean method
        """
        if DEBUG:
            print inspect.stack()[0][3]
        child = copy.copy(item1)
        if self.__attr.CHRO_IS_F is True:
            for i in range(self.__attr.N_CHROMOSOMES):
                child[i] = (item1[i]+item2[1])/2
        else:
            for i in range(self.__attr.N_CHROMOSOMES):
                f = (item1[i] + item2[i])/2
                child[i] = int(math.floor(f))
        if self.__attr.CAN_REPETEAD_CHRO is False:
            self.__Replace_repeated(child)
        return child

    def __Replace_repeated(self, child):
        """
            Function that replace the chromosomes repeated
        """
        if DEBUG:
            print inspect.stack()[0][3]
        n = self.__attr.CHRO_MINVALUE
        for i in range(0,len(child)-1):
            if child[i] in child[i + 1:]:
                while (True):
                    if n not in child:
                        child[i] = n
                        break
                    n += 1
        return child

    def __Generate_Child_split_tournament(self, item1, item2):
        """
            Funtion that generate 2 child and return the best of the parents and childs
        """
        if DEBUG:
            print inspect.stack()[0][3]
        childs=self.__Generate_Child_split(item1, item2)
        childs.append(item1)
        childs.append(item2)
        if self.__attr.TYPECHILD is CHILD_SPLIT_TOURNAMENT_DETERMINISTIC:
            return self.__Tournament_Selection_Deterministic(childs)
        elif self.__attr.TYPECHILD is CHILD_SPLIT_TOURNAMENT_PROBABILISTIC:
            return self.__Tournament_Selection_Probabilistic(childs)

    def __Generate_Child(self, item1, item2 = None):
        """
            Generate child main
        """
        if DEBUG:
            print inspect.stack()[0][3]
        if self.__attr.TYPECHILD is CHILD_FLIP:
            return self.__Generate_Child_flip(item1)
        elif self.__attr.TYPECHILD in [CHILD_FLIP_TOURNAMENT_DETERMINISTIC, CHILD_FLIP_TOURNAMENT_PROBABILISTIC]:
            return self.__Generate_Child_Flip_tournament(item1)
        elif self.__attr.TYPECHILD is CHILD_SPLIT:
            return self.__Generate_Child_split(item1, item2)
        elif self.__attr.TYPECHILD is CHILD_MEAN:
            return self.__Generate_Child_Mean(item1, item2)
        elif self.__attr.TYPECHILD in [CHILD_SPLIT_TOURNAMENT_DETERMINISTIC,CHILD_SPLIT_TOURNAMENT_PROBABILISTIC]:
            return self.__Generate_Child_split_tournament(item1, item2)

    def __Fill_Next_Generation(self):
        """
            Function that fill the pool
        """
        if DEBUG:
            print inspect.stack()[0][3]
        new_pull = copy.copy(self.__POOL)
        if self.__attr.TYPECHILD in types_childs_1:
            for i in (range(0, self.__attr.rangechild)):
                if(i is not self.__attr.rangechild):
                    child = self.__Generate_Child(copy.copy(self.__POOL[i][0]), item2 = self.__POOL[i+1][0])
                else:
                    child = self.__Generate_Child(copy.copy(self.__POOL[i][0]), item2=self.__POOL[i - 1][0])
                dest = i + self.__attr.sizeelitism
                if randint(0, 99) < self.__attr.MUTE:
                    child = self.mute_individuals(child)
                new_pull[dest][0] = copy.copy(child)
        elif self.__attr.TYPECHILD in types_childs_2:
            for i in (range(0, self.__attr.rangechild, 2)):
                if (i is not self.__attr.rangechild):
                    childs = self.__Generate_Child(copy.copy(self.__POOL[i][0]), item2 = copy.copy(self.__POOL[i + 1][0]))
                else:
                    childs = self.__Generate_Child(copy.copy(self.__POOL[i][0]), item2=self.__POOL[i - 1][0])
                dest = i + self.__attr.sizeelitism
                for j in [0,1]:
                    if randint(0, 99) < self.__attr.MUTE:
                        childs[j] = self.mute_individuals(childs[j])
                    new_pull[dest+j][0] = copy.copy(childs[j])
        return new_pull

    def __Tournament_Selection_Deterministic(self, listItems):
        """
            Function that select the best item from a list of items for tournament selection.
        """
        if DEBUG:
            print inspect.stack()[0][3]
        dict = [[0,0]for x in range(len(listItems))]
        for i in range(0, len(listItems)):
            dict[i][1] = self.__attr.FUN_FITNESS(listItems[i])
            dict[i][0] = listItems[i]
        dict.sort(key=self.__getKey,reverse=self.__attr.REVERSE)
        return dict[0][0]

    def __Tournament_Selection_Probabilistic(self, listItems):
        """
            Function that select the best item from a list of items for tournament selection.
        """
        if DEBUG:
            print inspect.stack()[0][3]
        return listItems[randint(0, len(listItems) - 1)]

    def __Roulette(self):
        """
            Function that selct the individuos to fill next pool
        """
        if DEBUG:
            print inspect.stack()[0][3]
        new_pool = copy.copy(self.__POOL)
        for i in (range(1, self.__attr.SIZE_POOL)):
            self.__POOL[i][1] = self.__POOL[i][1] + self.__POOL[i - 1][1]
        for i in (range(0, self.__attr.SIZE_POOL)):
            self.__POOL[i][2] = 1 - (self.__POOL[i][1] / self.__POOL[self.__attr.SIZE_POOL - 1][1])

        if self.__attr.TYPECHILD in types_childs_1:
            for i in (range(0, self.__attr.rangechild)):
                selec = random()
                for j in range(0, self.__attr.SIZE_POOL)[::-1]:
                    if selec < self.__POOL[j][2]:
                        break
                child = self.__Generate_Child(copy.copy(self.__POOL[j][0]),copy.copy(self.__POOL[j+1][0]))
                dest = i + self.__attr.sizeelitism
                if randint(0, 99) < self.__attr.MUTE:
                    child = self.mute_individuals(child)
                new_pool[dest][0] = copy.copy(child)
        elif self.__attr.TYPECHILD in types_childs_2:
            for i in (range(0, self.__attr.rangechild, 2)):
                selec1 = random()
                selec2 = random()
                for j in range(0, self.__attr.SIZE_POOL)[::-1]:
                    if selec1 < self.__POOL[j][2]:
                        break
                for k in range(0, self.__attr.SIZE_POOL)[::-1]:
                    if selec2 < self.__POOL[k][2]:
                        break
                childs = self.__Generate_Child(copy.copy(self.__POOL[j][0]), copy.copy(self.__POOL[k][0]))
                dest = i + self.__attr.sizeelitism
                for j in [0,1]:
                    if randint(0, 99) < self.__attr.MUTE:
                        childs[j] = self.mute_individuals(childs[j])
                    new_pool[dest+j][0] = copy.copy(childs[j])
        return new_pool

    def __Next_Generation(self):
        """
            Function main for fill next pool, this call the different forms the generate next pool
        """
        if DEBUG:
            print inspect.stack()[0][3]
        if self.__attr.SELECTION_TYPE is FILL_NEXT_GENERATION:
            self.__Fill_Next_Generation()
        elif self.__attr.SELECTION_TYPE is ROULETTE:
            self.__Roulette()

    def mute_individuals(self, item):
        """
            Function that mute a individuos
        """
        if DEBUG:
            print inspect.stack()[0][3]
        index = [randint(0, self.__attr.N_CHROMOSOMES - 1), randint(0, self.__attr.N_CHROMOSOMES - 1)]
        index.sort()
        a = copy.copy(item[index[0]:index[1]])
        b = copy.copy(item)
        b[index[0]:index[1]] = copy.copy(sample(a, len(b[index[0]:index[1]])))
        return b

    @QtCore.Slot()
    def __run(self):
        if DEBUG:
            print inspect.stack()[0][3]
        for i in range(self.__attr.SIZE_POOL):
            item = self.__Get_Individuos(i)
            self.__Set_Fittnes(i, self.__attr.FUN_FITNESS(item))
        self.__sort_pool(self.__attr.REVERSE)
        print "\rThe winer is: ", self.Winner_Probability()[1],
        self.__Next_Generation()

    def set_pool(self, pool):
        """
        Asign a predefined pool and activate testing mode
        If size of individual is not correct raise GenecticException
        :param pool: Is the population to be allocated: is of the type [[[individual],0,0],[[individual],0,0],...]
        """
        if DEBUG:
            print inspect.stack()[0][3]
        if self.__attr.N_CHROMOSOMES is not len(pool[0][0]):
            a = GenecticException
            a.what = "Error: the size of the individuos of pool is not correct."
            raise a
        self.__attr.TEST_POOL = True
        self.__POOL = copy.copy(pool)

    def get_empty_pool(self):
        """
        :return: a empty pool of the type [[[0 for x in range(self.___attr.N_CHROMOSOMES)], 0, 0] for y in range(self.__attr.SIZE_POOL)]
        """
        if DEBUG:
            print inspect.stack()[0][3]
        pool = [[[0 for x in range(self.__attr.N_CHROMOSOMES)], 0, 0] for y in range(self.__attr.SIZE_POOL)]
        return pool

    def get_pool(self):
        """
        :return: the current pool is of the type [[[individual],0,0],[[individual],0,0],...]
        """
        if DEBUG:
            print inspect.stack()[0][3]
        return copy.copy(self.__POOL)

    def print_individuals(self):
        """
            Print the individuals of the pool
        """
        if DEBUG:
            print inspect.stack()[0][3]
        for i in range(0, self.__attr.SIZE_POOL):
            print self.__POOL[i][:]

    def Winner_Probability(self):
        """
        :return: the current winning individual
        """
        if DEBUG:
            print inspect.stack()[0][3]
        return self.__POOL[0][:]

    def run(self, print_best=0):
        """
        Function main that run the algorithm
        :param print_best: If it is not 0, is printed top print_best
        """
        if DEBUG:
            print inspect.stack()[0][3]
        for x in range(self.__attr.ITMAX):
            for i in range(self.__attr.SIZE_POOL):
                item = self.__Get_Individuos(i)
                self.__Set_Fittnes(i, self.__attr.FUN_FITNESS(item))
            self.__sort_pool(self.__attr.REVERSE)
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

    def start(self,period=100):
        """
        Run a timer with period, this timer is connect with Function main that run the algorithm
        :param period:
        """
        if self.__attr.FUN_FITNESS is None:
            a = GenecticException
            a.what = "Error: It is necessary to initialize the parameters with setattrGeneticAlgorithm"
            raise a
        if DEBUG:
            print inspect.stack()[0][3]
        self.timer.start(period)

    def stop(self):
        """
        This function for the timer.
        """
        if DEBUG:
            print inspect.stack()[0][3]
        self.timer.stop()
