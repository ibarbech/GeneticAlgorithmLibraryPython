from GeneticAlgorithm.Genetic_Algorithm import *




class GeneticAlgorithm_Attr_t():

    def __init__(self, fun_fitness, chromosomes, itmax=50, child_type=CHILD_FLIP, selection_type=FILL_NEXT_GENERATION,
                 High_Low=False, size_pool=1000, porcent_elitism=10, porcent_mute=2, can_repeated_chro=False, testing=False):
        """
            Greate instance and set params to instance, this function can raise a GeneticException
            :param fun_fitness: is a pointer of function fitness
            :param chromosomes: is a class of chromosomes_t
            :param itmax: is a iteration max of funtion run
            :param child_type: is a type of generate the next pool
            :param selection_type: is a type of selection of individuos for generate the next pool
            :param High_Low: is True if you search a individual which function fintness is max
            :param size_pool: is the size of pool
            :param porcent_elitism: is the percentage you want to keep in the pool
            :param porcent_mute: is the percentage you want to keep in the group
            :param can_repeated_chro: is True if the crhomosomes of individual can be repeated
            :param testing:
            """
        if DEBUG:
            print inspect.stack()[0][3]
        if selection_type not in types_selection:
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
        if chromosomes.CHRO_IS_F is can_repeated_chro and can_repeated_chro is not False:
            a = GenecticException
            a.what = "Error: If var 'chromosomes.CHRO_IS_F' is true 'can_repeated_chro' must be true"
            raise a
        if child_type not in types_Child:
            a = GenecticException
            a.what = "Error: child_type is not correct"
            raise a
        try:
            self.ELITISM = porcent_elitism / 100.0
            self.MUTE = porcent_mute
            self.REVERSE = High_Low
            self.SELECTION_TYPE = selection_type
            self.SIZE_POOL = size_pool
            self.N_CHROMOSOMES = chromosomes.N_CHRO
            self.FUN_FITNESS = fun_fitness
            self.ITMAX = itmax
            self.TYPECHILD = child_type
            self.rangechild = (int)(self.SIZE_POOL - self.SIZE_POOL * self.ELITISM)-1
            self.sizeelitism = (int)(self.SIZE_POOL * self.ELITISM)
            self.CHRO_IS_F = chromosomes.CHRO_IS_F
            self.CHRO_MAXVALUE = chromosomes.MAXVALUE
            self.CHRO_MINVALUE = chromosomes.MINVALUE
            self.CAN_REPETEAD_CHRO = can_repeated_chro
            self.TEST_POOL = testing
        except:
            raise