
from PySide import QtCore,QtGui
import copy

RED = QtCore.Qt.red
BLUE = QtCore.Qt.blue
BLACK = QtCore.Qt.black
YELLOW = QtCore.Qt.yellow
GREEN = QtCore.Qt.green
class SCENE(QtGui.QGraphicsScene):
    def __init__(self):
        QtGui.QGraphicsScene.__init__(self)
        self.__N_cities=0
        self.__listCitys=[]

    def __draw_road(self,Road,pen):
        for i in range(len(Road) - 1):
            p1 = None
            p2 = None
            for x in self.__listCitys:
                if x[0] is Road[i]:
                    p1 = x[1]
                elif x[0] is Road[i + 1]:
                    p2 = x[1]
                if p1 is not None and p2 is not None:
                    break
            item = QtGui.QGraphicsLineItem(p1[0], p1[1], p2[0], p2[1])
            item.setPen(pen)
            self.addItem(item)
        p1 = None
        p2 = None
        for x in self.__listCitys:
            if x[0] is Road[0]:
                p1 = x[1]
            elif x[0] is Road[len(Road) - 1]:
                p2 = x[1]
            if p1 is not None and p2 is not None:
                break
        item = QtGui.QGraphicsLineItem(p1[0], p1[1], p2[0], p2[1])
        item.setPen(pen)
        self.addItem(item)

    def addCity(self,x,y):
        punto = copy.copy([self.__N_cities, [x, y]])
        self.__listCitys.append(punto)
        self.__N_cities+=1
        item=QtGui.QGraphicsEllipseItem(x-2,y-2,4,4)
        label = QtGui.QGraphicsTextItem(QtCore.QString(str(x[0])), item)
        label.moveBy(x[1][0], x[1][1])
        self.addItem(item)

    def Paint_road(self,Road1,color,size=1):
        pen=QtGui.QPen()
        pen.setColor(color);
        pen.setWidth(size);
        self.__draw_road(Road1,pen)

    def RePaint(self):
        for x in self.__listCitys:
            item = QtGui.QGraphicsEllipseItem(x[1][0]-5, x[1][1]-5, 10, 10)
            self.set_text(str(x[0]),x[1][0], x[1][1])
            self.addItem(item)

    def get_listCities(self):
        return copy.copy(self.__listCitys)

    def set_listCities(self,listcities):
        self.__listCitys = copy.copy(listcities)
        self.__N_cities = len(listcities)

    def set_text(self, text, x, y):
        label = QtGui.QGraphicsTextItem(text)
        label.moveBy(x, y)
        self.addItem(label)

    def Clear(self):
        self.clear()