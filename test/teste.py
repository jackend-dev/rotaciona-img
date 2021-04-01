# from PyQt5.QtWidgets import *
# import sys
#
# class Window(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)
#         layout = QGridLayout()
#         self.setLayout(layout)
#
#         radiobutton = QRadioButton("Australia")
#         radiobutton.setChecked(True)
#         radiobutton.value = 1
#         radiobutton.toggled.connect(self.onClicked)
#         layout.addWidget(radiobutton, 0, 0)
#
#         radiobutton = QRadioButton("China")
#         radiobutton.value = 2
#         radiobutton.toggled.connect(self.onClicked)
#         layout.addWidget(radiobutton, 0, 1)
#
#         radiobutton = QRadioButton("Japan")
#         radiobutton.value = 3
#         radiobutton.toggled.connect(self.onClicked)
#         layout.addWidget(radiobutton, 0, 2)
#
#     def onClicked(self):
#         radioButton = self.sender()
#         if radioButton.isChecked():
#             print("Country is %s" % (radioButton.value))
#
#
# app = QApplication(sys.argv)
# screen = Window()
# screen.show()
# sys.exit(app.exec_())

# import sys
# import time
#
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtWidgets import (QApplication, QDialog,
#                              QProgressBar, QPushButton, QMessageBox)
# from PyQt5.QtCore import QThread, pyqtSignal
#
# TIME_LIMIT = 100
#
#
# class External(QThread):
#     """
#         Runs a counter thread.
#         """
#
#     countChanged = pyqtSignal(int)
#
#     def run(self):
#         count = 0
#         while count < TIME_LIMIT:
#             count += 1
#             time.sleep(0.05)
#             self.countChanged.emit(count)
#             QMessageBox.setIconPixmap(QMessageBox.information(None, "Concluído", "10 imagens rotacionadas."),
#                                       QPixmap(":verificado.png"))
#             # QMessageBox.iconPixmap(QMessageBox.information(None, "Concluído", "10 imagens rotacionadas."))
#
# class Actions(QDialog):
#     """
#     Simple dialog that consists of a Progress Bar and a Button.
#     Clicking on the button results in the start of a timer and
#     updates the progress bar.
#     """
#
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Progress Bar')
#         self.progress = QProgressBar(self)
#         self.progress.setGeometry(0, 0, 300, 25)
#         self.progress.setMaximum(100)
#         self.button = QPushButton('Start', self)
#         self.button.move(0, 30)
#         self.show()
#
#         self.button.clicked.connect(self.onButtonClick)
#
#     def onButtonClick(self):
#         self.calc = External()
#         self.calc.countChanged.connect(self.onCountChanged)
#         self.calc.start()
#
#     def onCountChanged(self, value):
#         self.progress.setValue(value)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Actions()
#     sys.exit(app.exec_())

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time


# class MyThread(QThread):
#     # Create a counter thread
#     change_value = pyqtSignal(int)
#
#     def run(self):
#         cnt = 0
#         while cnt &100:
#             cnt += 1
#             time.sleep(0.3)
#             self.change_value.emit(cnt)
#
# class Window(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.title = "PyQt5 ProgressBar"
#         self.top = 200
#         self.left = 500
#         self.width = 300
#         self.height = 100
#         self.setWindowIcon(QtGui.QIcon("icon.png"))
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         vbox = QVBoxLayout()
#         self.progressbar = QProgressBar()
#         # self.progressbar.setOrientation(Qt.Vertical)
#         self.progressbar.setMaximum(100)
#         self.progressbar.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}"
#                                        "QProgressBar::chunk {background:yellow}")
#         # qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 red, stop: 1 white);
#         # self.progressbar.setStyleSheet("QProgressBar::chunk {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 red, stop: 1 white); }")
#         # self.progressbar.setTextVisible(False)
#         vbox.addWidget(self.progressbar)
#         self.button = QPushButton("Start Progressbar")
#         self.button.clicked.connect(self.startProgressBar)
#         self.button.setStyleSheet('background-color:yellow')
#         vbox.addWidget(self.button)
#         self.setLayout(vbox)
#         self.show()
#
#     def startProgressBar(self):
#         self.thread = MyThread()
#         self.thread.change_value.connect(self.setProgressVal)
#         self.thread.start()
#
#     def setProgressVal(self, val):
#         self.progressbar.setValue(val)
#
#
# App = QApplication(sys.argv)
# window = Window()
# sys.exit(App.exec())

import logging
import random
import sys
import time

from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logging.basicConfig(format="%(message)s", level=logging.INFO)

# 1. Subclass QRunnable
class Runnable(QRunnable):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def run(self):
        # Your long-running task goes here ...
        for i in range(5):
            logging.info(f"Working in thread {self.n}, step {i + 1}/5")
            time.sleep(random.randint(700, 2500) / 1000)

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("QThreadPool + QRunnable")
        self.resize(250, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        countBtn = QPushButton("Click me!")
        countBtn.clicked.connect(self.runTasks)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(countBtn)
        self.centralWidget.setLayout(layout)

    def runTasks(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText(f"Running {threadCount} Threads")
        pool = QThreadPool.globalInstance()
        for i in range(threadCount):
            # 2. Instantiate the subclass of QRunnable
            runnable = Runnable(i)
            # 3. Call start()
            pool.start(runnable)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())