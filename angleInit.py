from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QTextBrowser, QLabel,\
    QPushButton, QMessageBox, QStyle, qApp, QSpinBox, QDialogButtonBox, QLCDNumber, \
    QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot, QRect
from time import sleep
import configparser
import arMotor
import os

class angleInit(QDialog):
    def __init__(self, parent, instrument_list):
        super(angleInit, self).__init__(parent=parent)
        self.motor_pins = [12, 11, 10, 9]
        self.relay_pins = [2, 3, 4, 5]
        self.arduino = arMotor.ArduinoM(instrument_list[3], self.motor_pins, self.relay_pins)
        self.config = configparser.ConfigParser()
        self.dialog_angle = QDialog()
        self.dialog_angle.resize(507, 410)
        self.closeBox = QDialogButtonBox(self.dialog_angle)
        self.closeBox.setGeometry(QRect(150, 370, 341, 32))
        self.closeBox.setOrientation(Qt.Horizontal)
        self.closeBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.closeBox.accepted.connect(self.clickOK)
        self.closeBox.rejected.connect(self.dialog_angle.close)
        self.gridLayoutWidget = QWidget(self.dialog_angle)
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 481, 171))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_1 = QLabel(self.gridLayoutWidget)
        self.label_1.setText("Current Angle")
        self.gridLayout.addWidget(self.label_1, 0, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setText("Absolute noª of steps")

        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)

        self.lcdNumber_angle = QLCDNumber(self.gridLayoutWidget)

        self.gridLayout.addWidget(self.lcdNumber_angle, 1, 1, 1, 1)

        self.lcdNumber_steps = QLCDNumber(self.gridLayoutWidget)

        self.gridLayout.addWidget(self.lcdNumber_steps, 1, 3, 1, 1)

        self.gridLayoutWidget_2 = QWidget(self.dialog_angle)
        self.gridLayoutWidget_2.setGeometry(QRect(10, 190, 481, 61))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ccwise = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_ccwise.setText("Move counter clockwise")
        self.pushButton_ccwise.clicked.connect(self.move_ccwise)
        self.gridLayout_2.addWidget(self.pushButton_ccwise, 0, 1, 1, 1)

        self.pushButton_cwise = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_cwise.setText("Move clockwise")
        self.pushButton_cwise.clicked.connect(self.move_cwise)

        self.gridLayout_2.addWidget(self.pushButton_cwise, 0, 0, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.dialog_angle)
        self.horizontalLayoutWidget.setGeometry(QRect(10, 260, 481, 80))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setText("Angle step:")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox = QSpinBox(self.horizontalLayoutWidget)
        self.spinBox.setRange(-90, 90)

        self.horizontalLayout.addWidget(self.spinBox)

        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setText("Go")
        self.pushButton.clicked.connect(self.move_bystep)
        self.horizontalLayout.addWidget(self.pushButton)
        self.dialog_angle.show()

    def move_cwise(self):
        #Mueve de a 3 steps
        self.arduino.move_new(3, 0.05)
        self.lcdNumber_angle.display(self.arduino.steps_to_angle(self.arduino.steps_moved))
        self.lcdNumber_steps.display(self.arduino.steps_moved)

    def move_ccwise(self):
        self.arduino.move_new(-3, 0.05)
        self.lcdNumber_angle.display(self.arduino.steps_to_angle(self.arduino.steps_moved))
        self.lcdNumber_steps.display(self.arduino.steps_moved)

    def move_bystep(self):
        steps = self.arduino.angle_to_steps(self.spinBox.value())
        print("Motor will move by {} degs, steps = {}.".format(self.spinBox.value(), steps))
        self.arduino.move_new(steps, 0.05)
        self.lcdNumber_angle.display(self.arduino.steps_to_angle(self.arduino.steps_moved))
        self.lcdNumber_steps.display(self.arduino.steps_moved)

    def clickOK(self):
        if os.path.isfile("config.cfg"):
            self.config.read("config.cfg")
            self.arduino.steps_moved = 0
            self.config['DEFAULT']['motor_position'] = str(0)
            with open('config.cfg', 'w') as file:
                self.config.write(file)
            self.arduino.turnoff_motor()
            sleep(1)
            self.dialog_angle.close()
        else:
            # No deberia pasar, salvo que se borre en el medio el archivo de config.
            print("Config file not found. Did you delete it on purpose?"
                  "Re-run init instruments.")
            message = QMessageBox()
            ico = os.path.join(os.path.dirname(__file__), "icons/laika.png")
            pixmap = QPixmap(ico).scaledToHeight(128,
                                                 Qt.SmoothTransformation)
            message.setIconPixmap(pixmap)
            message.setWindowTitle("Error")
            message.setText("Config file not found. Did you delete it on purpose?\n"
                            "Close this window and re-run init instruments please.")
            message.setStandardButtons(QMessageBox.Ok)
            message.buttonClicked.connect(message.close)
            message.exec_()


