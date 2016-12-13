import os

from GeneticAlgorithm.Genetic_Algorithm import *
from GeneticAlgorithm.Genetic_Algorithm_attr import GeneticAlgorithm_Attr_t
from gui import *


def _checkStatetobool(checkbox):
    return checkbox.checkState() is QtCore.Qt.CheckState.Checked

def _getChildMode(index):
    childs_mode=[CHILD_FLIP,CHILD_SPLIT,CHILD_FLIP_TOURNAMENT_DETERMINISTIC,CHILD_FLIP_TOURNAMENT_PROBABILISTIC,CHILD_MEAN,
                 CHILD_SPLIT_TOURNAMENT_DETERMINISTIC,CHILD_SPLIT_TOURNAMENT_PROBABILISTIC]
    return childs_mode[index]

def _getSelectionMode(index):
    selections_mode=[FILL_NEXT_GENERATION,ROULETTE]
    return selections_mode[index]

class GeneticAlgorithm_gui(GeneticAlgorithm):

    def __init__(self):
        GeneticAlgorithm.__init__(self)
        #app = QtGui.QApplication(sys.argv)
        self.Dialog = QtGui.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        self.Dialog.showMaximized()
        QtCore.QTimer.connect(self.ui.Aceptar_Cancelar, QtCore.SIGNAL("accepted()"), self.Aceptar)
        QtCore.QTimer.connect(self.ui.Aceptar_Cancelar, QtCore.SIGNAL("rejected()"), self.Cancelar)
        self.Dialog.exec_()

        #app.exec_()

    def Aceptar(self):
        f = open("temp_Fun_fitness.py", 'w')
        f.write(self.ui.Funt_Fitness.toPlainText())
        f.close()
        import temp_Fun_fitness
        fun_fitness = temp_Fun_fitness.Fitness
        if _checkStatetobool(self.ui.Chrm_is_F):
            maxv = float(self.ui.Chrm_max.text())
            minv = float(self.ui.Chrm_min.text())
        else:
            maxv = int(self.ui.Chrm_max.text())
            minv = int(self.ui.Chrm_min.text())
        chrom = chromosome_t(self.ui.N_Chrom.value(), maxvalue=maxv, minvalue=minv,
                             chromosomes_is_float=_checkStatetobool(self.ui.Chrm_is_F))
        GA_attr=GeneticAlgorithm_Attr_t(fun_fitness, chromosomes=chrom, itmax=self.ui.Itmax.value(),
                                                 child_type=_getChildMode(self.ui.Child_mode.currentIndex()),
                                                 selection_type=_getSelectionMode(self.ui.Selection_mode.currentIndex()),
                                                 High_Low=_checkStatetobool(self.ui.High_Low),
                                                 size_pool=self.ui.Size_of_pool.value(),
                                                 porcent_elitism=self.ui.Elitism.value(), porcent_mute=self.ui.Mute.value(),
                                                 can_repeated_chro=_checkStatetobool(self.ui.Chrm_can_repetead))
        GeneticAlgorithm.setattrGeneticAlgorithm(self,GA_attr)

        self.Dialog.close()

    def Cancelar(self):
        self.Dialog.close()
        self.__del__()

    def __del__(self):
        try:
            os.remove("temp_Fun_fitness.py")
        except:
            pass


