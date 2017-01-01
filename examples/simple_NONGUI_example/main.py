from GeneticAlgorithm.Genetic_Algorithm import *

"""

Distance matrix between each city.
Used in the library to calculate each generation, fitness, etc.

"""

distance = [
    [9.22337203685e+18, 20.0, 15.0, 30.0, 25.0, 40.0, 30.0, 60.0, 50.0, 45.0],
    [20.0, 9.22337203685e+18, 30.0, 20.0, 15.0, 15.0, 20.0, 40.0, 40.0, 30.0],
    [15.0, 30.0, 9.22337203685e+18, 25.0, 30.0, 20.0, 30.0, 40.0, 45.0, 50.0],
    [30.0, 20.0, 25.0, 9.22337203685e+18, 20.0, 30.0, 10.0, 50.0, 40.0, 30.0],
    [25.0, 15.0, 30.0, 20.0, 9.22337203685e+18, 10.0, 20.0, 20.0, 30.0, 40.0],
    [40.0, 15.0, 20.0, 30.0, 10.0, 9.22337203685e+18, 20.0, 30.0, 20.0, 30.0],
    [30.0, 20.0, 30.0, 10.0, 20.0, 20.0, 9.22337203685e+18, 35.0, 40.0, 30.0],
    [60.0, 40.0, 40.0, 50.0, 20.0, 30.0, 35.0, 9.22337203685e+18, 30.0, 15.0],
    [50.0, 40.0, 45.0, 40.0, 30.0, 20.0, 40.0, 30.0, 9.22337203685e+18, 20.0],
    [45.0, 30.0, 50.0, 30.0, 40.0, 30.0, 30.0, 15.0, 20.0, 9.22337203685e+18]]

"""

Function defined to calculate the fitness of each individual
Used in the library - Necessary to past it to the Atributes

"""


def fitness(item):
    dist = 0
    cityant = item[0]
    for cityact in item[1:10]:
        dist = dist + distance[cityant][cityact]
        cityant = cityact
    dist = dist + distance[cityant][item[0]]
    return dist


GA = GeneticAlgorithm()

"""

        Call to configure the chromosome values.
        interval of values [minvalue,maxvalue)
        size of 10 chromosomes

"""
chrom = chromosome_t(10, maxvalue=10, minvalue=0,
                     chromosomes_is_float=True)

"""

Configure the attr of the algorithm, child gen, selection type,pool size, elitism, mutation, etc

"""
GA_attr = GeneticAlgorithm_Attr_t(fitness, chromosomes=chrom, itmax=1000,
                                  child_type=CHILD_FLIP,
                                  selection_type=FILL_NEXT_GENERATION,
                                  High_Low=False,
                                  size_pool=1000,
                                  porcent_elitism=10, porcent_mute=3,
                                  can_repeated_chro=False)
GA.setattrGeneticAlgorithm(GA_attr)

"""

Run the Genetic Algorithm Until the conditions are fulfilled

"""

GA.run()

"""

Print the best individual

"""
print GA.Winner_Probability()
