class chromosome_t():

    def __init__(self, n_chromosomes, maxvalue = None, minvalue = 0, chromosomes_is_float = False, ):
        """
        :param n_chromosomes: is the number of chromosomes that an individual has
        :param maxvalue: is the maximum value of a chromosome
        :param minvalue: is the minimum value of a chromosome
        :param chromosomes_is_float: is True if the value of a chromosome can be float
        """
        self.N_CHRO = n_chromosomes
        if maxvalue is None:
            self.MAXVALUE = n_chromosomes
        else:
            self.MAXVALUE = maxvalue
        self.MINVALUE = minvalue
        self.CHRO_IS_F = chromosomes_is_float