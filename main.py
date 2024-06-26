#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
import pyqtgraph as pg
import numpy as np
from pathlib import Path
from datetime import date
from csv import writer, QUOTE_NONE
from time import sleep
from measureThreads import AngleThread, FieldThread, SensThread
from initInst import InitializeInstruments
from angleInit import angleInit
__version__ = "1.0"


class Ui_MainWindow(QMainWindow):
    showMessage_saturation = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__()
        self.threadpool = QThreadPool()
        self.setupUi()
        self.sample_saturated = False

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"HallRober")
        self.resize(579, 600)
        # Main widget
        self.centralwidget = QWidget(self)
        self.comboBox_measure = QComboBox(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout_grid = QGridLayout(self.centralwidget)
        self.label = QLabel(self.centralwidget)
        self.label.setText("Filename:")
        self.label.setGeometry(QRect(10, 10, 62, 13))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setText('Sample Name')
        self.label_2.setGeometry(QRect(10, 50, 91, 16))
        self.lineEdit_fname = QLineEdit(self.centralwidget)
        self.lineEdit_fname.setGeometry(QRect(80, 0, 381, 27))
        # Combobox measures
        self.comboBox_measure.addItems(["Angle Sweep", "Custom Angle V vs H", "Sensitivity"])
        self.comboBox_measure.setGeometry(QRect(170, 80, 151, 28))
        self.comboBox_measure.activated.connect(self.change_layout)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setText("Type of measurement:")
        self.label_3.setGeometry(QRect(10, 90, 141, 16))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QRect(110, 40, 191, 27))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setText('Browse...')
        self.pushButton.setGeometry(QRect(470, 0, 91, 29))
        self.pushButton.clicked.connect(self.save_Filename)

        # Adding these layouts to mainLayout_grid:
        self.mainLayout_grid.addWidget(self.label, 0, 0)
        self.mainLayout_grid.addWidget(self.lineEdit_fname, 0, 1)
        self.mainLayout_grid.addWidget(self.pushButton, 0, 2)
        self.mainLayout_grid.addWidget(self.label_2, 1, 0)
        self.mainLayout_grid.addWidget(self.lineEdit_2, 1, 1)
        self.mainLayout_grid.addWidget(self.label_3, 2, 0)
        self.mainLayout_grid.addWidget(self.comboBox_measure, 2, 1)
        # Adding mainLayout_grid to mainLayout:
        self.mainLayout.addLayout(self.mainLayout_grid)

        # Layouts for the different possible measurements
        self.stackedLayout = QStackedLayout()
        # Angle sweep layout
        self.AngleSweep = QWidget(self.centralwidget)
        self.AngleSweep.setGeometry(QRect(10, 120, 551, 421))
        #Central Layout
        self.AngleSweep_layout = QVBoxLayout(self.AngleSweep)
        self.AngleSweep_layout.setSizeConstraint(QLayout.SetNoConstraint)
        #Grid layout
        self.AngleSweep_glayout = QGridLayout(self.AngleSweep)
        # Widgets de AngleSweep_glayout:
        self.label_4 = QLabel(self.AngleSweep)
        self.label_4.setText(u"Start angle")
        self.AngleSweep_glayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.spinBox = QSpinBox(self.AngleSweep)
        self.spinBox.setRange(-90, 90)
        self.AngleSweep_glayout.addWidget(self.spinBox, 0, 1, 1, 1)
        self.label_7 = QLabel(self.AngleSweep)
        self.label_7.setText(u"Current (in uA)")
        self.AngleSweep_glayout.addWidget(self.label_7, 0, 2, 1, 1)
        self.spinBox_4 = QSpinBox(self.AngleSweep)
        self.spinBox_4.setRange(0, 30000)
        self.spinBox_4.setSingleStep(5)
        self.AngleSweep_glayout.addWidget(self.spinBox_4, 0, 3, 1, 1)
        self.label_5 = QLabel(self.AngleSweep)
        self.label_5.setText(u"End angle")
        self.AngleSweep_glayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.spinBox_2 = QSpinBox(self.AngleSweep)
        self.spinBox_2.setRange(0, 360)
        self.AngleSweep_glayout.addWidget(self.spinBox_2, 1, 1, 1, 1)
        self.label_9 = QLabel(self.AngleSweep)
        self.label_9.setText(u"Number of measurements:")
        self.AngleSweep_glayout.addWidget(self.label_9, 1, 2, 1, 1)
        self.spinBox_6 = QSpinBox(self.AngleSweep)
        self.spinBox_6.setRange(1, 50)
        self.spinBox_6.setSingleStep(1)
        self.AngleSweep_glayout.addWidget(self.spinBox_6, 1, 3, 1, 1)
        self.label_6 = QLabel(self.AngleSweep)
        self.label_6.setText(u"Angle step")
        self.AngleSweep_glayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.spinBox_3 = QSpinBox(self.AngleSweep)
        self.spinBox_3.setRange(1, 15)
        self.AngleSweep_glayout.addWidget(self.spinBox_3, 2, 1, 1, 1)
        self.label_8 = QLabel(self.AngleSweep)
        self.label_8.setText(u"Applied field (G)")
        self.AngleSweep_glayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.spinBox_5 = QSpinBox(self.AngleSweep)
        self.spinBox_5.setRange(-300, 300)
        self.spinBox_5.setValue(-300)
        self.spinBox_5.setSingleStep(50)
        self.AngleSweep_glayout.addWidget(self.spinBox_5, 2, 3, 1, 1)
        self.label_10 = QLabel(self.AngleSweep)
        self.label_10.setText(u"Estimated time:")
        self.AngleSweep_glayout.addWidget(self.label_10, 3, 0, 1, 1)
        self.label_11 = QLabel(self.AngleSweep)
        self.label_11.setText(u"..")
        self.AngleSweep_glayout.addWidget(self.label_11, 3, 1, 1, 1)
        # "START" button config for AngleSweep
        self.pushButton_2 = QPushButton(self.AngleSweep)
        self.pushButton_2.setToolTip("You have to initialize the instruments first.")
        self.pushButton_2.setDisabled(True)
        self.pushButton_2.setText("Start")
        self.pushButton_2.pressed.connect(lambda: self.start_meas("Angle"))
        self.AngleSweep_glayout.addWidget(self.pushButton_2, 3, 2, 1, 1)
        # STOP button
        self.pushButton_2s = QPushButton(self.AngleSweep)
        self.pushButton_2s.setCheckable(True)
        self.pushButton_2s.setDisabled(True)
        self.pushButton_2s.setText("Stop")
        self.AngleSweep_glayout.addWidget(self.pushButton_2s, 3, 3, 1, 1)
        # Add grid layout to main AngleSweep Layout
        self.AngleSweep_layout.addLayout(self.AngleSweep_glayout)
        self.AngleSweep_layout.addLayout(self.AngleSweep_glayout)
        # Plot Layout
        self.AngleSweep_plotLayout = QVBoxLayout(self.AngleSweep)
        self.plotwid = pg.PlotWidget(self.AngleSweep)
        self.plotwid.setBackground('w')
        self.plotwid_curve = pg.ScatterPlotItem(size=5,
                                                brush=pg.mkBrush(30, 255, 0, 255))

        self.plotwid.addItem(self.plotwid_curve)
        self.plotwid.setLabel('left', 'Hall Voltage [V]')
        self.plotwid.setLabel('bottom', 'Angle (Deg)')
        self.AngleSweep_plotLayout.addWidget(self.plotwid)

        self.statusLabel_a = QLabel(self.AngleSweep)
        self.statusLabel_a.setText("Ready")
        self.AngleSweep_plotLayout.addWidget(self.statusLabel_a)
        # Add plot layout to main AngleSweep Layout
        self.AngleSweep_layout.addLayout(self.AngleSweep_plotLayout)
        self.AngleSweep.setLayout(self.AngleSweep_layout)
        self.stackedLayout.addWidget(self.AngleSweep)

        ###################################
        # Single angle V vs H layout
        self.FieldSweep = QWidget(self.centralwidget)
        self.FieldSweep.setGeometry(QRect(10, 120, 551, 421))
        self.FieldSweep_layout = QVBoxLayout(self.FieldSweep)
        self.FieldSweep_layout.setSizeConstraint(QLayout.SetNoConstraint)
        self.FieldSweep_glayout = QGridLayout(self.FieldSweep)
        # Widgets for grid layout
        self.label_1b = QLabel(self.FieldSweep)
        self.label_1b.setText("Starting Field (G)")
        self.FieldSweep_glayout.addWidget(self.label_1b, 0, 0, 1, 1)
        self.spinBox_2b = QSpinBox(self.FieldSweep)
        self.spinBox_2b.setSingleStep(50)
        self.spinBox_2b.setRange(-300, 300)
        self.spinBox_2b.setValue(-300)
        self.FieldSweep_glayout.addWidget(self.spinBox_2b, 0, 1, 1, 1)
        self.label_3b = QLabel(self.FieldSweep)
        self.label_3b.setText("Angle (deg)")
        self.FieldSweep_glayout.addWidget(self.label_3b, 0, 2, 1, 1)
        self.spinBox_4b = QSpinBox(self.FieldSweep)
        self.spinBox_4b.setRange(0, 90)
        self.FieldSweep_glayout.addWidget(self.spinBox_4b, 0, 3, 1, 1)
        self.label_5b = QLabel(self.FieldSweep)
        self.label_5b.setText("End Field (G)")
        self.FieldSweep_glayout.addWidget(self.label_5b, 1, 0, 1, 1)
        self.spinBox_6b = QSpinBox(self.FieldSweep)
        self.spinBox_6b.setRange(-300, 300)
        self.spinBox_6b.setValue(300)
        self.spinBox_6b.setSingleStep(10)
        self.FieldSweep_glayout.addWidget(self.spinBox_6b, 1, 1, 1, 1)
        self.label_7b = QLabel(self.FieldSweep)
        self.label_7b.setText("Number of measurements")
        self.FieldSweep_glayout.addWidget(self.label_7b, 1, 2, 1, 1)
        self.spinBox_8b = QSpinBox(self.FieldSweep)
        self.spinBox_8b.setRange(1, 50)
        self.spinBox_8b.setSingleStep(1)
        self.FieldSweep_glayout.addWidget(self.spinBox_8b, 1, 3, 1, 1)
        self.label_9b = QLabel(self.FieldSweep)
        self.label_9b.setText("Field Step (G)")
        self.FieldSweep_glayout.addWidget(self.label_9b, 2, 0, 1, 1)
        self.spinBox_10b = QDoubleSpinBox(self.FieldSweep)
        self.spinBox_10b.setRange(0.1, 20)
        self.spinBox_10b.setSingleStep(0.1)
        self.FieldSweep_glayout.addWidget(self.spinBox_10b, 2, 1, 1, 1)
        self.label_11b = QLabel(self.FieldSweep)
        self.label_11b.setText("Current (uA)")
        self.FieldSweep_glayout.addWidget(self.label_11b, 2, 2, 1, 1)
        self.spinBox_12b = QSpinBox(self.FieldSweep)
        self.spinBox_12b.setSingleStep(5)
        self.spinBox_12b.setRange(0, 30000)
        self.FieldSweep_glayout.addWidget(self.spinBox_12b, 2, 3, 1, 1)
        self.label_13b = QLabel(self.FieldSweep)
        self.label_13b.setText(u"Estimated time:")
        self.FieldSweep_glayout.addWidget(self.label_13b, 3, 0, 1, 1)
        self.label_14b = QLabel(self.FieldSweep)
        self.label_14b.setText(u"..")
        self.FieldSweep_glayout.addWidget(self.label_14b, 3, 1, 1, 1)
        self.pushButton_15b = QPushButton(self.FieldSweep)
        self.pushButton_15b.setText("Start")
        self.pushButton_15b.setToolTip("You need to initialize the instruments first.")
        self.pushButton_15b.setDisabled(True)
        # STOP button
        self.pushButton_15s = QPushButton(self.AngleSweep)
        self.pushButton_15s.setCheckable(True)
        self.pushButton_15s.setDisabled(True)
        self.pushButton_15s.setText("Stop")
        self.pushButton_15b.pressed.connect(lambda: self.start_meas("Field"))
        self.FieldSweep_glayout.addWidget(self.pushButton_15b, 3, 2, 1, 1)
        self.FieldSweep_glayout.addWidget(self.pushButton_15s, 3, 3, 1, 1)
        self.FieldSweep_layout.addLayout(self.FieldSweep_glayout)
        # Plot for the Field sweep
        self.FieldSweep_plotLayout = QVBoxLayout(self.FieldSweep)
        self.plotwid_2 = pg.PlotWidget(self.FieldSweep)
        self.plotwid_2_curve = pg.ScatterPlotItem(size=5,
                                                  brush=pg.mkBrush(200, 0, 30, 200))
        self.plotwid_2.addItem(self.plotwid_2_curve)
        self.plotwid_2.setBackground('w')
        self.plotwid_2.setLabel('left', 'Hall Voltage [V]')
        self.plotwid_2.setLabel('bottom', 'Field (G)')
        self.FieldSweep_plotLayout.addWidget(self.plotwid_2)
        self.statusLabel_b = QLabel(self.FieldSweep)
        self.statusLabel_b.setText("Ready")
        self.FieldSweep_plotLayout.addWidget(self.statusLabel_b)
        self.FieldSweep_layout.addLayout(self.FieldSweep_plotLayout)
        self.FieldSweep.setLayout(self.FieldSweep_layout)
        self.stackedLayout.addWidget(self.FieldSweep)


        ###################################
        # Sensitivity layout
        self.SensSweep = QWidget(self.centralwidget)
        self.SensSweep.setGeometry(QRect(10, 120, 551, 421))
        self.SensSweep_layout = QVBoxLayout(self.SensSweep)
        self.SensSweep_layout.setSizeConstraint(QLayout.SetNoConstraint)
        self.SensSweep_glayout = QGridLayout(self.SensSweep)
        # Widgets for grid layout
        self.label_s1 = QLabel(self.SensSweep)
        self.label_s1.setText("Saturation Field (G)")
        self.SensSweep_glayout.addWidget(self.label_s1, 0, 0, 1, 1)
        self.spinBox_s2 = QSpinBox(self.SensSweep)
        self.spinBox_s2.setSingleStep(5)
        self.spinBox_s2.setRange(-300, 300)
        self.spinBox_s2.setValue(-300)
        self.SensSweep_glayout.addWidget(self.spinBox_s2, 0, 1, 1, 1)
        self.label_s3 = QLabel(self.SensSweep)
        self.label_s3.setText("Start Field (G)")
        self.SensSweep_glayout.addWidget(self.label_s3, 1, 0, 1, 1)
        self.spinBox_s4 = QDoubleSpinBox(self.SensSweep)
        self.spinBox_s4.setRange(-2, 2)
        self.spinBox_s4.setValue(-1)
        self.spinBox_s4.setSingleStep(0.1)
        self.SensSweep_glayout.addWidget(self.spinBox_s4, 1, 1, 1, 1)
        self.label_s5 = QLabel(self.SensSweep)
        self.label_s5.setText("End Field (G)")
        self.SensSweep_glayout.addWidget(self.label_s5, 2, 0, 1, 1)
        self.spinBox_s6 = QDoubleSpinBox(self.SensSweep)
        self.spinBox_s6.setRange(-2, 2)
        self.spinBox_s6.setValue(1)
        self.spinBox_s6.setSingleStep(0.1)
        self.SensSweep_glayout.addWidget(self.spinBox_s6, 2, 1, 1, 1)
        self.label_s7 = QLabel(self.SensSweep)
        self.label_s7.setText(u"Angle:")
        self.SensSweep_glayout.addWidget(self.label_s7, 3, 0, 1, 1)

        self.spinBox_s8 = QSpinBox(self.SensSweep)
        self.spinBox_s8.setRange(0, 360)
        self.spinBox_s8.setValue(0)
        self.SensSweep_glayout.addWidget(self.spinBox_s8, 3, 1, 1, 1)

        self.label_s9 = QLabel(self.SensSweep)
        self.label_s9.setText("Field Step (G)")
        self.SensSweep_glayout.addWidget(self.label_s9, 0, 2, 1, 1)
        self.spinBox_s10 = QDoubleSpinBox(self.SensSweep)
        self.spinBox_s10.setRange(-1, 1)
        self.spinBox_s10.setSingleStep(0.05)
        self.spinBox_s10.setValue(0.1)
        self.SensSweep_glayout.addWidget(self.spinBox_s10, 0, 3, 1, 1)

        self.label_s11 = QLabel(self.SensSweep)
        self.label_s11.setText("Current (uA)")
        self.SensSweep_glayout.addWidget(self.label_s11, 1, 2, 1, 1)
        self.spinBox_s12 = QSpinBox(self.SensSweep)
        self.spinBox_s12.setSingleStep(5)
        self.spinBox_s12.setRange(0, 30000)
        self.SensSweep_glayout.addWidget(self.spinBox_s12, 1, 3, 1, 1)

        self.label_s13 = QLabel(self.SensSweep)
        self.label_s13.setText("Number of Measurements")
        self.SensSweep_glayout.addWidget(self.label_s13, 2, 2, 1, 1)

        self.spinBox_s14 = QSpinBox(self.SensSweep)
        self.spinBox_s14.setRange(1, 30)
        self.spinBox_s14.setSingleStep(1)
        self.SensSweep_glayout.addWidget(self.spinBox_s14, 2, 3, 1, 1)

        self.pushButton_s15 = QPushButton(self.SensSweep)
        self.pushButton_s15.setText("Start")
        self.pushButton_s15.setToolTip("You need to initialize the instruments first.")
        self.pushButton_s15.setDisabled(True)
        # STOP button
        self.pushButton_s16 = QPushButton(self.AngleSweep)
        self.pushButton_s16.setCheckable(True)
        self.pushButton_s16.setDisabled(True)
        self.pushButton_s16.setText("Stop")
        self.pushButton_s15.pressed.connect(lambda: self.start_meas("Sensitivity"))

        self.SensSweep_glayout.addWidget(self.pushButton_s15, 3, 2, 1, 1)
        self.SensSweep_glayout.addWidget(self.pushButton_s16, 3, 3, 1, 1)
        self.SensSweep_layout.addLayout(self.SensSweep_glayout)
        # Plot for the Field sweep
        self.SensSweep_plotLayout = QVBoxLayout(self.SensSweep)
        self.plotwid_s = pg.PlotWidget(self.SensSweep)
        self.plotwid_s_curve = pg.ScatterPlotItem(size=5,
                                                  brush=pg.mkBrush(100, 20, 100, 200)
                                                  )
        self.plotwid_s.addItem(self.plotwid_s_curve)
        self.plotwid_s.setBackground('w')
        self.plotwid_s.setLabel('left', 'Hall Voltage [V]')
        self.plotwid_s.setLabel('bottom', 'Field (G)')
        self.SensSweep_plotLayout.addWidget(self.plotwid_s)
        self.statusLabel_s19 = QLabel(self.SensSweep)
        self.statusLabel_s19.setText("Ready")
        self.SensSweep_plotLayout.addWidget(self.statusLabel_s19)
        self.SensSweep_layout.addLayout(self.SensSweep_plotLayout)
        self.SensSweep.setLayout(self.SensSweep_layout)
        self.stackedLayout.addWidget(self.SensSweep)
        #########################################################

        #########################################################
        self.mainLayout.addLayout(self.stackedLayout)
        self.centralwidget.setLayout(self.mainLayout)


        # Menu bar
        menubar = self.menuBar()
        fileMenu = QMenu("&File", self)
        helpMenu = QMenu("&Help", self)
        menubar.addMenu(fileMenu)
        menubar.addMenu(helpMenu)
        selectFile_menu = QAction("Select Filename", fileMenu)
        instrument_menu = QAction("Initialize instruments", fileMenu)
        saveang_menu = QAction("Save V vs Angle measurements", fileMenu)
        savefield_menu = QAction("Save V vs Field measurments", fileMenu)
        savesens_menu = QAction("Save Sensor Sensitivity measurment", fileMenu)
        setangle_menu = QAction("Set Angle", fileMenu)
        about_menu = QAction("About HallRober", helpMenu)
        fileMenu.addAction(selectFile_menu)
        fileMenu.addAction(instrument_menu)
        fileMenu.addAction(saveang_menu)
        fileMenu.addAction(savefield_menu)
        fileMenu.addAction(savesens_menu)
        fileMenu.addAction(setangle_menu)
        helpMenu.addAction(about_menu)
        selectFile_menu.triggered.connect(self.save_Filename)
        instrument_menu.triggered.connect(self.initialize_instr_func)
        saveang_menu.triggered.connect(lambda: self.write_file(meas='Angle'))
        savefield_menu.triggered.connect(lambda: self.write_file(meas='Field'))
        savesens_menu.triggered.connect(lambda: self.write_file(meas='Sensitivity'))
        setangle_menu.triggered.connect(self.set_angle)
        about_menu.triggered.connect(self.helpAbout)
    # ENDsetupUi

    @pyqtSlot()
    def initialize_instr_func(self):
        # We get the instruments' addresses with this func.
        self.insts_init = InitializeInstruments(self)
        self.insts_init.setModal(True)
        self.insts_init.signals.isconfig.connect(self.inst_init_finished)
        # We can access the insts' address list afterwards with:
        # (e.g) self.instrument_list

    @pyqtSlot()
    def set_angle(self):
        # We get the instruments' addresses with this func.
        try:
            self.insts_init.instrument_list
        except NameError:
            print("Instruments have not been initialized yet.")
            message = QMessageBox()
            ico = os.path.join(os.path.dirname(__file__), "icons/laika.png")
            pixmap = QPixmap(ico).scaledToHeight(128,
                                                 Qt.SmoothTransformation)
            message.setIconPixmap(pixmap)
            message.setWindowTitle("Error")
            message.setText("Arduino has not been properly initialized.\n"
                            "Please do so by running the \"Initialize Instruments\" \n"
                            "command first.")
            message.setStandardButtons(QMessageBox.Ok)
            message.buttonClicked.connect(message.close)
            message.exec_()
        else:
            if not self.insts_init.instrument_list:
                print("Arduino not been properly initialized yet.")
                message = QMessageBox()
                ico = os.path.join(os.path.dirname(__file__), "icons/laika.png")
                pixmap = QPixmap(ico).scaledToHeight(128,
                                                     Qt.SmoothTransformation)
                message.setIconPixmap(pixmap)
                message.setWindowTitle("Error")
                message.setText("Arduino has not been properly initialized.\n"
                                "Please do so by running the \"Initialize Instruments\" \n"
                                "command first.")
                message.setStandardButtons(QMessageBox.Ok)
                message.buttonClicked.connect(message.close)
                message.exec_()
            else:
                self.angle_init = angleInit(self, self.insts_init.instrument_list)
                self.angle_init.setModal(True)

    def helpAbout(self):
        msg = QMessageBox.about(self, "About HallRober",
                                    """<b>HallRober - Measuring Planar Hall Effect & AMR.</b> 
                                    <p>Version %s (2024) by Agostina Lo Giudice.
                                    (agostina.logiudice@gmail.com)
                                    <p>This program is distributed under the GNU 
                                    Public License v3.
                                    """ % __version__)

    def save_Filename(self):
        # Open FileDialog to get save file name.
        p = os.path.expanduser("~")
        filename, _ = QFileDialog.getSaveFileName(self, "Select a File",
                                                  p,
                                                  r"CSV files (*.csv)")
        if filename:
            path = Path(filename)
            self.lineEdit_fname.setText(str(path))
            print('File path: {}'.format(path))

    def write_file(self, meas):
        # Writing the obtained results to a file.
        try:
            file = open(self.lineEdit_fname.text(), 'w')
        except:
            warn = QMessageBox()
            warn.setWindowTitle('Error: Invalid or missing filename')
            ico = os.path.join(os.path.dirname(__file__), "icons/laika.png")
            pixmap = QPixmap(ico).scaledToHeight(64,
                                                Qt.SmoothTransformation)
            warn.setIconPixmap(pixmap)
            warn.setText('No filename specified, or invalid filename!\n'
                         'Please try again.')
            warn.setStandardButtons(QMessageBox.Ok)
            warn.buttonClicked.connect(warn.close)
            warn.exec_()
        else:
            if meas == 'Angle':
                contents = [['Date: {}'.format(date.today())],
                            ['Sample name: {}'.format(self.lineEdit_2.text())],
                            ['Type of Measurement: {}'.format(self.comboBox_measure.currentText())],
                            ['-DATA START-'],
                            ['Applied Current: {} uA'.format(self.spinBox_4.value())],
                            ['Applied Field: {} G'.format(self.spinBox_5.value())],
                            ['Number of Measurements per angle: {}'.format(self.spinBox_6.value())],
                            ['Start Angle: {} deg'.format(self.spinBox.value())],
                            ['End Angle: {} deg'.format(self.spinBox_2.value())],
                            ['Angle Step: {} deg'.format(self.spinBox_3.value())]
                            ]
                wr = writer(file, delimiter=',', quoting=QUOTE_NONE, escapechar='\\')
                for row in contents:
                    wr.writerow(row)
                wr.writerow(['Angle (deg),Hall Voltage (V),Voltage std (V)'])
                data = zip(self.angle_sweep, self.volt_angsweep, self.volt_angsweep_std)
                wr.writerows(data)
                self.update_legend_a('Data written to {}'.format(self.lineEdit_fname.text()))
                print('Data written to {}'.format(self.lineEdit_fname.text()))
                file.close()
            elif meas == 'Field':
                contents = [['Date: {}'.format(date.today())],
                            ['Sample name: {}'.format(self.lineEdit_2.text())],
                            ['Type of Measurement: {}'.format(self.comboBox_measure.currentText())],
                            ['-DATA START-'],
                            ['Applied Current: {} uA'.format(self.spinBox_12b.value())],
                            ['Sample Angle: {} G'.format(self.spinBox_4b.value())],
                            ['Number of Measurements per Field: {}'.format(self.spinBox_8b.value())],
                            ['Start Field: {} G'.format(self.spinBox_2b.value())],
                            ['End Field: {} G'.format(self.spinBox_6b.value())],
                            ['Field Step: {} G'.format(self.spinBox_10b.value())]
                            ]
                wr = writer(file, delimiter=',', quoting=QUOTE_NONE, escapechar='\\')
                for row in contents:
                    wr.writerow(row)
                wr.writerow(['Field (deg),Hall Voltage (V),Voltage std (V)'])
                data = zip(self.total_field, self.volt_fieldsweep, self.volt_fieldsweep_std)
                wr.writerows(data)
                self.update_legend_s('Data written to {}'.format(self.lineEdit_fname.text()))
                print('Data written to {}'.format(self.lineEdit_fname.text()))
                file.close()
            elif meas == 'Sensitivity':
                contents = [['Date: {}'.format(date.today())],
                            ['Sample name: {}'.format(self.lineEdit_2.text())],
                            ['Type of Measurement: {}'.format(self.comboBox_measure.currentText())],
                            ['-DATA START-'],
                            ['Applied Current: {} uA'.format(self.spinBox_s12.value())],
                            ['Sample Angle: {} G'.format(self.spinBox_s8.value())],
                            ['Number of Measurements per Field: {}'.format(self.spinBox_s14.value())],
                            ['Saturation Field: {} G'.format(self.spinBox_s2.value())],
                            ['Start Field: {} G'.format(self.spinBox_s4.value())],
                            ['End Field: {} G'.format(self.spinBox_s6.value())],
                            ['Field Step: {} G'.format(self.spinBox_s10.value())]
                            ]
                wr = writer(file, delimiter=',', quoting=QUOTE_NONE, escapechar='\\')
                for row in contents:
                    wr.writerow(row)
                wr.writerow(['Field (deg),Hall Voltage (V),Voltage std (V)'])
                data = zip(self.sens_sweep, self.volt_senssweep, self.volt_senssweep_std)
                wr.writerows(data)
                print('Data written to {}'.format(self.lineEdit_fname.text()))
                self.update_legend_s('Data written to {}'.format(self.lineEdit_fname.text()))
                file.close()


    def change_layout(self):
        #Change layout when "measure" combobox is changed
        self.stackedLayout.setCurrentIndex(self.comboBox_measure.currentIndex())

    def start_meas(self, meas_type):
        # Starting the worker threads for each different type of measurement.
        if meas_type == "Angle":
            #Disable "START" button for Field and Angle measurements.
            # 15b = start button for Field meas
            # 2 = start button for Angle meas
            # 2s = stop button for Angle meas
            self.plotwid_curve.clear()
            self.pushButton_15b.setDisabled(True)
            self.pushButton_2.setDisabled(True)
            self.pushButton_s15.setDisabled(True)
            self.pushButton_2s.setEnabled(True)
            sleep(2)
            ## Thread start
            # Define the list of angles we will sweep through.
            # Pasamos los valores de ang inicial, final y step al thread
            self.angle_array = [self.spinBox.value(), self.spinBox_2.value(), self.spinBox_3.value()]
            self.angle_sweep = []
            self.volt_angsweep = []
            self.volt_angsweep_std = []
            current = self.spinBox_4.value() * 10 ** (-6)
            field = self.spinBox_5.value()
            num_meas = self.spinBox_6.value()
            self.worker = AngleThread(var1=self.angle_array, var2=field,
                                      var3=current, var4=num_meas,
                                      var5=self.insts_init.instrument_list)
            self.worker.signals.result.connect(self.update_plot_angle)
            self.worker.signals.result2.connect(self.update_legend_a)
            self.worker.signals.finished.connect(self.thread_complete)
            self.pushButton_2s.clicked.connect(self.worker.finish_run)
            self.threadpool.start(self.worker)

        elif meas_type == "Field":
            self.plotwid_2_curve.clear()
            # Disable "START" button for Field and Angle measurements.
            # 15b = start button for Field meas
            # 2 = start button for Angle meas
            # 15s = stop button for Field meas
            self.pushButton_15b.setDisabled(True)
            self.pushButton_2.setDisabled(True)
            self.pushButton_s15.setDisabled(True)
            self.pushButton_15s.setEnabled(True)

            sleep(2)
            ## Thread start
            # Define the list of angles we will sweep through.
            self.field_sweep = np.arange(self.spinBox_2b.value(),
                                        self.spinBox_6b.value()+1,
                                        self.spinBox_10b.value()
                                        )
            self.total_field = np.concatenate((self.field_sweep, np.flip(self.field_sweep)))
            # Array in which we'll store the measured voltage.
            self.volt_fieldsweep = []
            self.volt_fieldsweep_std = []
            current = self.spinBox_12b.value() * 10 ** (-6)
            angle = self.spinBox_4b.value()
            num_meas = self.spinBox_8b.value()
            self.worker = FieldThread(var1=self.field_sweep, var2=current,
                                      var3=angle, var4=num_meas,
                                      var5=self.insts_init.instrument_list)
            self.worker.signals.result.connect(self.update_plot_field)
            self.worker.signals.result2.connect(self.update_legend_b)
            self.worker.signals.finished.connect(self.thread_complete)
            self.pushButton_15s.clicked.connect(self.worker.finish_run)
            self.threadpool.start(self.worker)

        elif meas_type == 'Sensitivity':
            self.plotwid_s_curve.clear()
            # Disable "START" button for Field and Angle measurements.
            # 15b = start button for Field meas
            # 2 = start button for Angle meas
            # 15s = stop button for Field meas
            self.pushButton_15b.setDisabled(True)
            self.pushButton_2.setDisabled(True)
            self.pushButton_s16.setEnabled(True)
            sleep(2)
            ## Thread start
            # Define the list of angles we will sweep through.
            self.sens_sweep = np.arange(self.spinBox_s4.value(),
                                         self.spinBox_s6.value(),
                                         self.spinBox_s10.value()
                                         )
            # Hacemos un ida y vuelta de la corriente (only for testing purposes)
            # Si no sirve, hay que resaturar y volver
            self.sens_sweep = np.concatenate((self.sens_sweep, np.flip(self.sens_sweep)))
            # Array in which we'll store the measured voltage & field.
            self.volt_senssweep = []
            self.volt_senssweep_std = []
            current = self.spinBox_s12.value() * 10 ** (-6)
            angle = self.spinBox_s8.value()
            num_meas = self.spinBox_s14.value()
            saturation_f = self.spinBox_s2.value()
            self.worker = SensThread(self, var1=self.sens_sweep, var2=current,
                                     var3=angle, var4=num_meas,
                                     var5=self.insts_init.instrument_list,
                                     var6=saturation_f)

            self.showMessage_saturation.connect(self.cable_change_dialog)
            self.worker.signals.result.connect(self.update_plot_sens)
            self.worker.signals.result2.connect(self.update_legend_s)
            self.worker.signals.finished.connect(self.thread_complete)
            self.pushButton_s16.clicked.connect(self.worker.finish_run)
            #self.signal.dialog_closed.connect(self.worker.sample_saturated)
            self.threadpool.start(self.worker)

    def cable_change_dialog(self):
        warn = QMessageBox()
        warn.setWindowTitle('Change DC source connection')
        ico = os.path.join(os.path.dirname(__file__), "icons/warn.png")
        pixmap = QPixmap(ico).scaledToHeight(64,
                                             Qt.SmoothTransformation)
        warn.setIconPixmap(pixmap)
        warn.setText('Sample has been saturated. Please connect the Keithley\n'
                     'source to the H Coils, and an external current source to the\n'
                     'sample.')
        warn.setStandardButtons(QMessageBox.Ok)
        warn.buttonClicked.connect(lambda: self.close_and_change(warn))
        warn.exec_()

    def close_and_change(self, dialog):
        dialog.close()
        print("Dialog closed")
        self.sample_saturated = True

    def update_legend_a(self, stri):
        self.statusLabel_a.setText(stri)

    def update_legend_b(self, stri):
        self.statusLabel_b.setText(stri)

    def update_legend_s(self, stri):
        self.statusLabel_s19.setText(stri)

    def update_plot_angle(self, s):
        self.plotwid_curve.addPoints([s[0]], [s[1]])
        self.angle_sweep.append(s[0])
        self.volt_angsweep.append(s[1])
        self.volt_angsweep_std.append(s[2])

    def update_plot_field(self, s):
        self.plotwid_2_curve.addPoints([s[0]], [s[1]])
        self.volt_fieldsweep.append(s[1])
        self.volt_fieldsweep_std.append(s[2])

    def update_plot_sens(self, s):
        self.plotwid_s_curve.addPoints([s[0]], [s[1]])
        self.volt_senssweep.append(s[1])
        self.volt_senssweep_std.append(s[2])

    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.statusLabel_a.setText("Finished.")
        self.statusLabel_b.setText("Finished.")
        self.statusLabel_s19.setText("Finished.")
        # Enable all start buttons again
        self.pushButton_2.setEnabled(True)
        self.pushButton_15b.setEnabled(True)
        self.pushButton_s15.setEnabled(True)
        finished = QMessageBox()
        ico = os.path.join(os.path.dirname(__file__), "icons/medium.png")
        pixmap = QPixmap(ico).scaledToHeight(128,
                                             Qt.SmoothTransformation)
        finished.setIconPixmap(pixmap)
        finished.setWindowTitle("Finished")
        finished.setText('Measurement has\n finished '
                        'successfully!')
        finished.setStandardButtons(QMessageBox.Ok)
        finished.buttonClicked.connect(finished.close)
        finished.exec_()

    def inst_init_finished(self):
        # This function should be run when the "Initialize Instruments"
        # has been completed successfully
        # In that case, the "START" buttons should be enabled.
        print("Signal received from InitInst")
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setToolTip("Start V vs Angle measurement.")
        self.pushButton_15b.setEnabled(True)
        self.pushButton_15b.setToolTip("Start V vs Field measurement")
        self.pushButton_s15.setEnabled(True)
        self.pushButton_s15.setToolTip("Start sensitivity measurement.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("HallRober - version %s" % __version__)
    app.setOrganizationDomain("www.github.com/alogiudice/hallrober")
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__),
                                               "icons/rober.png")))
    form = Ui_MainWindow()
    form.show()
    app.exec_()

