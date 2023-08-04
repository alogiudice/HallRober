from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QTextBrowser, QLabel,\
    QPushButton, QMessageBox, QStyle, qApp, QSpinBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot
from time import sleep
import pyvisa
import re
import configparser
import os

class angleInit(QDialog):
    def __init__(self, parent):
        super(angleInit, self).__init__(parent=parent)
        self.config = configparser.ConfigParser()
        self.dialog_angle = QDialog()
        self.dialog_angle.setWindowTitle("Set new angle")
        frame_angle = QVBoxLayout(self.dialog_angle)
        grid_angle = QGridLayout(self.dialog_angle)
        init_text = QLabel()
        self.config.read("config.cfg")
        self.current_position = self.config['DEFAULT']['motor_position']
        self.current_angle = float(self.current_position) * 512 / 360
        init_text.setText("Current position:{} ({} deg)".format(self.current_position, round(self.current_angle)))
        button_CW = QPushButton()
        # setting geometry of button
        button_CW.setGeometry(200, 150, 100, 30)
        button_CW.clicked.connect(self.clickme)
        ico_CW = os.path.join(os.path.dirname(__file__), "icons/curled_CW.png")
        button_CW.setStyleSheet("background-image : ico_CW;")
        button_CCW = QPushButton()
        # setting geometry of button
        button_CCW.setGeometry(200, 150, 100, 30)
        button_CCW.clicked.connect(self.clickme)
        ico_CCW = os.path.join(os.path.dirname(__file__), "icons/curled_CCW.png")
        button_CCW.setStyleSheet("background-image : ico_CCW;")
        labelCW = QLabel()
        labelCW.setText('Move Clockwise by 5deg')
        labelCCW = QLabel()
        labelCW.setText('Move Counter-Clockwise by 5deg')
        label_movebyAng = QLabel()
        label_movebyAng.setText('Move by Angle:')
        angle_spin = QSpinBox()
        angle_spin.setRange(-90, 90)
        angle_spin.setSingleStep(1)
        button_move = QPushButton()
        button_move.setText('Go')
        frame_angle.addWidget(init_text)
        frame_angle.addLayout(grid_angle)
        grid_angle.addWidget(button_CW, 0, 0, 2, 2)
        grid_angle.addWidget(button_CCW, 0, 1, 2, 2)
        grid_angle.addWidget(labelCW, 1, 0, 1, 1)
        grid_angle.addWidget(labelCCW, 1, 1, 1, 1)
        grid_angle.addWidget(label_movebyAng, 2, 0, 1, 1)
        grid_angle.addWidget(angle_spin, 2, 1, 1, 1)
        grid_angle.addWidget(button_move, 2, 2, 1, 1)
        self.dialog_angle.setLayout(frame_angle)
        self.dialog_angle.setFixedSize(400, 400)
        self.dialog_angle.show()

    def clickme(self):
        pass


