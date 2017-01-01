from GeneticAlgorithm import GeneticAlgorithm_gui
import sys
from PySide import QtGui

app = QtGui.QApplication(sys.argv)
GA= GeneticAlgorithm_gui.GeneticAlgorithm_gui()

GA.run()

print GA.Winner_Probability()