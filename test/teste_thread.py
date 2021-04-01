# from tqdm import tqdm
# import time
#
# for i in tqdm(range(161),
#               desc="Loading…",
#               ascii=False, ncols=100):
#     time.sleep(0.01)
#
# print("Complete.")

# log_ = open(os.path.join(os.path.dirname(self.script_dir_borrar), 'log_p.txt'),'r')
# log_a = log_.readline()
# log_.close()
# total = log_a.split("/")[1]
# current = log_a.split("/")[0]
# #print(os.path.join(os.path.dirname(self.script_dir), 'log_a.txt'))
# #if(self.dlg.ql_init_borrar.text()!='' or self.dlg.ql_init_borrar.text()!='NULL' or self.dlg.ql_init_borrar.text()!=None):
# percent = 100*abs(int(self.dlg.ql_init.text())-int(current))/(int(total)-int(self.dlg.ql_init.text()))
# if(float(percent)<1):
# percent=1.0
# #print(log_a, " ", percent)
# self.dlg.label_.setText(log_a)
# self.dlg.progressBar_.setValue(percent)
# self.timer=QTimer()
#        self.timer.start(250)
#        self.timer.timeout.connect(self.update)

# from progress_ui import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, time

class Ui_Dialog(object):
  def setupUi(self, MainWindow):
      MainWindow.setObjectName("MainWindow")
      MainWindow.resize(923, 619)
      self.centralwidget = QtWidgets.QWidget(MainWindow)
      self.centralwidget.setObjectName("centralwidget")
      MainWindow.setCentralWidget(self.centralwidget)
      self.statusbar = QtWidgets.QStatusBar(MainWindow)
      self.statusbar.setObjectName("statusbar")
      self.statusbar.showMessage('Welcome!')
      MainWindow.setStatusBar(self.statusbar)
      self.retranslateUi(MainWindow)
      QtCore.QMetaObject.connectSlotsByName(MainWindow)

  def retranslateUi(self, MainWindow):
      _translate = QtCore.QCoreApplication.translate
      MainWindow.setWindowTitle(_translate("MainWindow", "Test"))

class mythread(QtCore.QThread):
    def __init__(self,parent,n):
        QtCore.QThread.__init__(self,parent)
        self.n=n

    def run(self):
        self.emit(QtCore.SIGNAL("total(PyQt_PyObject)"),self.n)
        i=0
        while (i<self.n):
            if (time.time() % 1==0):
                i+=1
                #print str(i)
                self.emit(QtCore.SIGNAL("update()"))

# create the dialog for zoom to point
class progress(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.progressBar.setValue(0)
        self.t=mythread(self,100)
        QtCore.QObject.connect(self.t, QtCore.SIGNAL("total(PyQt_PyObject)"), self.total)
        QtCore.QObject.connect(self.t, QtCore.SIGNAL("update()"), self.update)
        self.n=0
        self.t.start()
    def update(self):
        self.n+=1
        print(self.n)
        self.ui.progressBar.setValue(self.n)
    def total(self,total):
        self.ui.progressBar.setMaximum(total)

if __name__=="__main__":
    app = QtGui.QApplication([])
    c=progress()
    c.show()
    sys.exit(app.exec_())