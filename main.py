import sys
from PyQt6.QtWidgets import QApplication
from windows.mainwindow import MainWindow
from os import path as p, mkdir
if not p.exists(p.dirname(p.abspath(__file__)) + "/img/icnoutput"):
    mkdir(p.dirname(p.abspath(__file__)) + "/img/icnoutput")
if not p.exists(p.dirname(p.abspath(__file__)) + "/img/icnoutput/icons"):
    mkdir(p.dirname(p.abspath(__file__)) + "/img/icnoutput/icons")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
