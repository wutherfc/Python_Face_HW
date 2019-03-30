import sys
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import func
import cv2
import base64
from windows import Welcome_Window, Detect_Window, Merge_Window, Compare_Window, Scene_Window
import qdarkstyle

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 1000, 600)

        self.setStyleSheet(qdarkstyle.load_stylesheet())
        #palette = QPalette()
        #palette.setBrush(self.backgroundRole(), QBrush(QPixmap('./welcome.jpg')))
        #self.setPalette(palette)


        self.start_Welcome()

    def start_Welcome(self):
        self.Welcome = Welcome_Window()
        self.setWindowTitle('Welcome')
        self.setCentralWidget(self.Welcome)
        self.Welcome.send.sendMsg.connect(self.updateWindow)
        self.show()

    def updateWindow(self, msg):
        print(msg)
        if msg['option1'] == '人脸识别':
            if msg['option2'] == 'Face-Detect':
                self.start_Detect()
            elif msg['option2'] == 'Face-Compare':
                self.start_Compare()
        elif msg['option1'] == '场景识别':
            if msg['option2'] == 'Scene-Detect':
                self.start_Scene()
        elif msg['option1'] == '人脸融合':
            if msg['option2'] == 'Face-Merge':
                self.start_Merge()
        elif msg['option1'] == '0':
            self.start_Welcome()

    def start_Detect(self):
        self.Detect = Detect_Window()
        self.setWindowTitle('Detect')
        self.setCentralWidget(self.Detect)
        self.Detect.send.sendMsg.connect(self.updateWindow)
        self.show()

    def start_Compare(self):
        self.Compare = Compare_Window()
        self.setWindowTitle('Compare')
        self.setCentralWidget(self.Compare)
        self.Compare.send.sendMsg.connect(self.updateWindow)
        self.show()

    def start_Scene(self):
        self.Scene = Scene_Window()
        self.setWindowTitle('Scene')
        self.setCentralWidget(self.Scene)
        self.Scene.send.sendMsg.connect(self.updateWindow)
        self.show()

    def start_Merge(self):
        self.Merge = Merge_Window()
        self.setWindowTitle('Merge')
        self.setCentralWidget(self.Merge)
        self.Merge.send.sendMsg.connect(self.updateWindow)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
