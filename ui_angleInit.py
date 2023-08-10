# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'angleInitsELgah.ui'
##
## Created by: Qt User Interface Compiler version 5.15.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(507, 410)
        self.closeBox = QDialogButtonBox(Dialog)
        self.closeBox.setObjectName(u"closeBox")
        self.closeBox.setGeometry(QRect(150, 370, 341, 32))
        self.closeBox.setOrientation(Qt.Horizontal)
        self.closeBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 481, 171))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_1 = QLabel(self.gridLayoutWidget)
        self.label_1.setObjectName(u"label_1")

        self.gridLayout.addWidget(self.label_1, 0, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)

        self.lcdNumber_angle = QLCDNumber(self.gridLayoutWidget)
        self.lcdNumber_angle.setObjectName(u"lcdNumber_angle")

        self.gridLayout.addWidget(self.lcdNumber_angle, 1, 1, 1, 1)

        self.lcdNumber_steps = QLCDNumber(self.gridLayoutWidget)
        self.lcdNumber_steps.setObjectName(u"lcdNumber_steps")

        self.gridLayout.addWidget(self.lcdNumber_steps, 1, 3, 1, 1)

        self.gridLayoutWidget_2 = QWidget(Dialog)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 190, 481, 61))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ccwise = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_ccwise.setObjectName(u"pushButton_ccwise")

        self.gridLayout_2.addWidget(self.pushButton_ccwise, 0, 1, 1, 1)

        self.pushButton_cwise = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_cwise.setObjectName(u"pushButton_cwise")

        self.gridLayout_2.addWidget(self.pushButton_cwise, 0, 0, 1, 1)

        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 260, 481, 80))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox = QSpinBox(self.horizontalLayoutWidget)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout.addWidget(self.spinBox)

        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.retranslateUi(Dialog)
        self.closeBox.accepted.connect(Dialog.accept)
        self.closeBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_1.setText(QCoreApplication.translate("Dialog", u"Current Angle", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Current no of steps", None))
        self.pushButton_ccwise.setText(QCoreApplication.translate("Dialog", u"Move counter clockwise", None))
        self.pushButton_cwise.setText(QCoreApplication.translate("Dialog", u"Move clockwise", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Angle step:", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Go", None))
    # retranslateUi

