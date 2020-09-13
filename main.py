import sys  # sys нужен для передачи argv в QApplication
import os  # Для отображения содержимого директорий
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import design_2  # Файл дизайна
import imutils
import cv2
import qimage2ndarray
import numpy


class EGApp(QtWidgets.QMainWindow, QtWidgets.QGraphicsView, design_2.Ui_MainWindow):
    def __init__(self):
        # Для доступа к переменным, методам и т.д. в файле design.py

        
        super().__init__()
        self.setupUi(self)  # Для инициализации дизайна
        self.btnBrowse.clicked.connect(self.browse_folder)          # поиск по папкам
        self.factory2Button.clicked.connect(self.f2_folder)         # открыть папку 5-фабрики
        self.factory5Button.clicked.connect(self.f5_folder)         # открыть папку 5-фабрики
        self.t_floorButton.clicked.connect(self.tf_folder)          # открыть папку Тех. этажа
        self.zagot_Button.clicked.connect(self.zagot_folder)        # открыть папку Заготівельний
        self.ccs_Button.clicked.connect(self.ccs_folder)            # открыть папку ЦХШ
        self.instr_Button.clicked.connect(self.instr_folder)        # открыть папку Инструментального
        self.treeWidget.clicked.connect(self.choose)                # выбрать из дерева
        self.listWidget.itemClicked.connect(self.setPath)           # по клику на файл в списке собрать путь

    def choose(self):
        self.column = [(self.treeWidget.topLevelItem(0).text(0)), (self.treeWidget.currentItem().text(0))]  # папка Ф2 и имя файла
        self.path = ('./Schem/' + self.column[0] + '/' + self.column[-1] + '.jpg')
        print (self.path)
        if (self.column[-1] != 'Фабрика-5') and (self.column[-1] != 'Фабрика-2') and (self.column[-1] != 'ТехПоверх') and (self.column[-1] != 'ЦХШ') and (self.column[-1] != 'Інструментальний'):
        
            if os.path.exists(self.path):
                print ('1')
            else:
                self.column = [(self.treeWidget.topLevelItem(1).text(0)), (self.treeWidget.currentItem().text(0))]  # папка Ф5 и имя файла
                self.path = ('./Schem/' + self.column[0] + '/' + self.column[-1] + '.jpg')
                print (self.path)
           
            if os.path.exists(self.path):
                print ('2')
            else:
                self.column = [(self.treeWidget.topLevelItem(2).text(0)), (self.treeWidget.currentItem().text(0))]  # папка ТехПоверх и имя файла
                self.path = ('./Schem/' + self.column[0] + '/' + self.column[-1] + '.jpg')
                print (self.path)
            if os.path.exists(self.path):
                print ('3')
            else:
                self.column = [(self.treeWidget.topLevelItem(3).text(0)), (self.treeWidget.currentItem().text(0))]  # папка Заготівельний и имя файла
                self.path = ('./Schem/' + self.column[0] + '/' + self.column[-1] + '.jpg')
                print (self.path)
            if os.path.exists(self.path):
                print ('4')
            else:
                self.column = [(self.treeWidget.topLevelItem(4).text(0)), (self.treeWidget.currentItem().text(0))]  # папка Инструментального и имя файла
                self.path = ('./Schem/' + self.column[0] + '/' + self.column[-1] + '.jpg')
                print (self.path)
            if os.path.exists(self.path):
                print ('5')
            else:
                self.column = [(self.treeWidget.topLevelItem(5).text(0)), (self.treeWidget.currentItem().text(0))]  # папка ЦХШ и имя файла
                self.path = ('./Schem/' + self.column[0] + '/' + self.column[-1] + '.jpg')
                print (self.path)
            self.resizePic()

    def browse_folder(self):
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории
        self.showDir()
    
    def f2_folder(self):
        self.directory = './Schem/Фабрика-2'
        self.showDir()

    def f5_folder(self):
        self.directory = './Schem/Фабрика-5'
        self.showDir()

    def tf_folder(self):
        self.directory = './Schem/ТехПоверх'
        self.showDir()

    def zagot_folder(self):
        self.directory = './Schem/Заготівельний цех'
        self.showDir()

    def ccs_folder(self):
        self.directory = './Schem/ЦХШ'
        self.showDir()

    def instr_folder(self):
        self.directory = './Schem/Інструментальний'
        self.showDir()

    def showDir(self):
        print (self.directory)

        self.listWidget.clear()
        for file_name in os.listdir(self.directory):    # для каждого файла в директории
            self.listWidget.addItem(file_name)          # добавить файл в listWidget
    
    def setPath(self):  # собираем путь для окна поиска
        self.file = (self.listWidget.currentItem().text())
        print (self.directory)
        print (self.file)
        self.path = self.directory + '/' + self.file
        print (self.path)
        self.resizePic()

    def resizePic(self):    # подгоняем размер картинки
        self.stream = open(self.path, "rb")                                  # читаем файл и отдаем OpenCV
        bytes = bytearray(self.stream.read())                                # он сам тупой и не умеет
        self.numpyarray = numpy.asarray(bytes, dtype=numpy.uint8)            # кирилицу в именах
        self.frame = cv2.imdecode(self.numpyarray, cv2.IMREAD_UNCHANGED)
        self.frame = imutils.resize(self.frame, width=800)
        self.path = qimage2ndarray.array2qimage(self.frame)
        self.showPic()

    def showPic(self):
        self.win = QWidget()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()

        self.view.setScene(self.scene)
        self.scene.addPixmap(QPixmap(self.path))
        self.scene.setBackgroundBrush(QBrush(Qt.white, Qt.SolidPattern))

        hbox = QGridLayout(self)
        hbox.addWidget(self.view, 2, 2)

        self.win.setLayout(hbox)
        self.win.show()
        self.file = ()
        #self.path = ()
       


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = EGApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
