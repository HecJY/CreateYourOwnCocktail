# @Date    : 2019-11/11
# @Author  : James(Jiaxing) Yang
# @File	   : AnGuiApp.py
# @Version : $0.1$



import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from GUI.result import *
from back_end.load_cocktail_recp import *
import os
from back_end.execution import *

class resultAPP(QMainWindow, Ui_Form_R):
    def __init__(self, parent =None):
        #initiallize
        super(resultAPP, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        #init
        self.parent = parent
        self.init_text()
        self.no_btn.clicked.connect(self.back)
        self.satisify_btn.clicked.connect(self.yes)

    def init_text(self):
        self.result_box.setFontPointSize(15)
        out = "The Predicted Sources are:\n"
        out += ";".join(self.parent.grad_r)
        out += "\n\nThe suggested amount for each material is:\n"
        ind = 0
        for x in self.parent.amount_r:
            source = self.parent.grad_r[ind]
            out += source + ": " + "; ".join(set(x[:3])) + "\n"
            ind += 1
        out += "\n\nThe suggested actions for each material is:\n"
        for x in self.parent.action_r:
            valid = list()
            for y in self.parent.action_r[x]:
                if self.parent.action_r[x][y] > 0:
                    valid.append(y)

            out += x + ": " + "; ".join(set(valid[:3])) + "\n"


        self.result_box.setText(out)


    def back(self):
        self.close()
        self.parent.child = None
        self.parent.show()

    def yes(self):
        #add items for re-training
        add_on = dict()
        add_on[self.cock_tail_name.text()] = self.parent.final
        self.parent.g2g.append(add_on)
        self.close()
        self.parent.child = None
        self.parent.show()






if __name__ == "__main__":
    App = QApplication(sys.argv)
    first_layerForm = resultAPP()
    first_layerForm.show()

    sys.exit(App.exec_())