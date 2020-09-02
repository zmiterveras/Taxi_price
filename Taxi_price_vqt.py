#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        ico = QtGui.QIcon('taxi_logo_16.png')
        self.setWindowIcon(ico)
        self.win = MyWindow()
        self.setCentralWidget(self.win)
        menuBar = self.menuBar()
        myMenu = menuBar.addMenu('&Menu')
        action = myMenu.addAction('&Расчитать',  self.win.countresult)
        action.setStatusTip('Расчет затрат')
        action = myMenu.addAction('&О программе', self.win.info)
        action.setStatusTip('Информация о программе' )
        myMenu.addSeparator()
        action = myMenu.addAction('&Выход', QtWidgets.qApp.quit)
        action.setStatusTip('Выход из программы')
        statusBar = self.statusBar()
        statusBar.showMessage('"Taxi price" приветствует вас', 5000)
        

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.makeWidget()
        
        
    def makeWidget(self):
        self.vbox = QtWidgets.QVBoxLayout()
        self.probeg()
        self.tarif()
        self.hbox = QtWidgets.QHBoxLayout()
        actlist = [('Ok', self.countresult),('Info', self.info),('Quit', QtWidgets.qApp.quit)]
        for name, act in actlist:
            btn = QtWidgets.QPushButton(name)
            btn.clicked.connect(act)
            self.hbox.addWidget(btn)
        self.vbox.addWidget(self.box1)
        self.vbox.addWidget(self.box2)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
           
    def probeg(self):
        self.box1 = QtWidgets.QGroupBox('Пробеги')
        self.box1.setAlignment(QtCore.Qt.AlignHCenter)
        self.entries = []
        names = ['Пробег город', 'Пробег трасса',
                 'Средняя поездка город',
                 'Средняя поездка трасса']
        for name in names:
            spin = QtWidgets.QSpinBox()
            spin.setSuffix(' км')
            spin.setRange(0,100000)
            self.entries.append((spin, name))
        self.entries[0][0].setSingleStep(100)
        self.entries[1][0].setSingleStep(100)
        self.form1 = QtWidgets.QFormLayout()
        for (sp, n)  in self.entries:
            self.form1.addRow(n, sp)
        boximage = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel()
        label.setPixmap(QtGui.QPixmap('auto.png'))
        boximage.addWidget(label)
        boximage.addLayout(self.form1)
        self.box1.setLayout(boximage)
        #self.box1.setLayout(self.form1)
            
    def tarif(self):
        self.box2 = QtWidgets.QGroupBox('Тарифы такси')
        self.box2.setAlignment(QtCore.Qt.AlignHCenter)                
        self.tentries = []
        tnames = ['Тариф город', 'Тариф загород',
                  'Посадка']
        for name in tnames:
            dspin = QtWidgets.QDoubleSpinBox()
            dspin.setSuffix(' руб')
            dspin.setSingleStep(0.01)
            self.tentries.append((dspin, name))
        self.form2 = QtWidgets.QFormLayout()
        self.spin = QtWidgets.QSpinBox()
        self.spin.setSuffix(' км')
        for (sp, n)  in self.tentries:
            self.form2.addRow(n, sp)
        self.form2.addRow('Включенные км', self.spin)
        boximage = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel()
        label.setPixmap(QtGui.QPixmap('taxi_PNG5.png'))
        boximage.addWidget(label)
        boximage.addLayout(self.form2)
        self.box2.setLayout(boximage)
        #self.box2.setLayout(self.form2)
           
    def countresult(self):
        res = []
        ent = self.entries + self.tentries
        ent.append((self.spin, ''))
        for name in ent:
            d = name[0].value()
            if type(d) == float:
                d = round(d,2)
            res.append(d)
        self.result(res)
                
    def result(self,name):
        try:
            Pcity = (name[0]/name[2])*name[6] + (name[0] - name[7]*(name[0]/name[2]))*name[4]
            Proute = (name[1]/name[3])*name[6] +(name[1] - name[7]*(name[1]/name[3]))*name[5]
        except ZeroDivisionError:
            QtWidgets.QMessageBox.warning(window, 'Предупреждение', 'Введены недопустимые нулевые значения')
            return
        P = Pcity + Proute
        mes = "Затраты: %s руб\nВ том числе:\n  Город: %s руб\n  За городом: %s руб"
        QtWidgets.QMessageBox.information(window, 'Результаты', mes % (P, Pcity, Proute))
        
    def info(self):
        msg = "Данная программа позволяет\nопределить затраты на\nпользование такси"
        QtWidgets.QMessageBox.information(window,'О программе', msg)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Taxi price')
    window.show()
    sys.exit(app.exec_()) 