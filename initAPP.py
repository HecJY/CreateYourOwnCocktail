# @Date    : 2019-11/11
# @Author  : James(Jiaxing) Yang
# @File	   : AnGuiApp.py
# @Version : $0.1$



import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from GUI.init import *
from back_end.load_cocktail_recp import *
import os
from back_end.execution import *
from resultAPP import *

class initAPP(QMainWindow, Ui_Form):
    def __init__(self):
        #initiallize
        super(initAPP, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        #init
        self.g2g, self.g2a, self.g2t = grad_grad()
        self.create_btn.clicked.connect(self.backend)
        self.show_source.clicked.connect(self.file)
        self.child = None

    def get_val(self):
        self.ctx_size = self.num_src.text()
        self.main_source = self.sources.text()

    def backend(self):
        self.get_val()
        self.grad_r, self.amount_r, self.action_r = back_end(self.ctx_size, self.main_source, self.g2g, self.g2a, self.g2t)
        self.child = resultAPP(parent = self)
        self.close()
        self.child.show()


    def file(self):
        os.startfile("all_gradients.txt")



if __name__ == "__main__":
    App = QApplication(sys.argv)
    first_layerForm = initAPP()
    first_layerForm.show()

    sys.exit(App.exec_())