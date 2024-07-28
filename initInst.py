import equipos as inst
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QTextBrowser, QLabel, \
    QComboBox, QPushButton, QMessageBox, QStyle, qApp
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot
from time import sleep
import pyvisa
import re
import configparser
import os
import serial.tools.list_ports

class ComboBox(QComboBox):
    #Override the common ComboBox to automatically filter duplicates
    def addItem(self, item):
        if item not in self.get_set_items():
            super(ComboBox, self).addItem(item)
        if item is None:
            pass
        if not str(item):
            pass

    def addItems(self, items):
        items = list(self.get_set_items() | set(items))
        super(ComboBox, self).addItems(items)

    def get_set_items(self):
        return set([self.itemText(i) for i in range(self.count())])

class initInstSignals(QObject):
    # Because the implementation of signals in pyqt is absolute sh*t
    # PyQt9 has come out, and we STILL have to define signals outside of init
    # if not it doesn't work. yay
    isconfig = pyqtSignal(str)

class InitializeInstruments(QDialog):
    def __init__(self, parent):
        super(InitializeInstruments, self).__init__(parent=parent)
        self.config = configparser.ConfigParser()
        # If no config file is present, we create a new one
        # List the different instruments connected to the PC.
        self.arduino_PID = '2341:0043'
        self.signals = initInstSignals()
        self.ports = serial.tools.list_ports.comports()
        self.rm = pyvisa.ResourceManager('@py')
        self.info = list(self.rm.list_resources())
        self.dialog_inst = QDialog()
        self.dialog_inst.setWindowTitle("Instruments")
        frame_inst = QVBoxLayout(self.dialog_inst)
        init_text = QLabel()
        init_text.setText("Available Instruments:")
        inputs = QGridLayout(self.dialog_inst)
        text_inst_output = QTextBrowser(self.dialog_inst)
        label1 = QLabel(self.dialog_inst)
        label1.setText('As multimeter, use:')
        self.choice1 = ComboBox(self.dialog_inst)
        label2 = QLabel(self.dialog_inst)
        label2.setText('As current source for sample, use:')
        self.choice2 = ComboBox(self.dialog_inst)
        label3 = QLabel(self.dialog_inst)
        label3.setText('As current source for coils, use:')
        self.choice3 = ComboBox(self.dialog_inst)
        label4 = QLabel(self.dialog_inst)
        label4.setText('As an Arduino for the motor, use:')
        self.choice4 = ComboBox(self.dialog_inst)
        who1 = self.create_who_button()
        who2 = self.create_who_button()
        who3 = self.create_who_button()
        who4 = self.create_who_button()
        self.status_label = QLabel()
        self.status_label.setText("test")

        i = 0
        for item in self.info:
            text_inst_output.append('{}) address: {}\n'.format(i, item))
            print(item)
            self.choice1.addItem(item)
            self.choice2.addItem(item)
            self.choice3.addItem(item)
            self.choice4.addItem(item)
            i += 1
        self.choice1.setCurrentIndex(1)
        self.choice2.setCurrentIndex(1)
        self.choice3.setCurrentIndex(1)
        self.choice4.setCurrentIndex(1)
        frame_inst.addWidget(init_text)
        frame_inst.addWidget(text_inst_output)
        inputs.addWidget(label1, 0, 0, 1, 1)
        inputs.addWidget(self.choice1, 0, 1, 1, 1)
        inputs.addWidget(who1, 0, 2, 1, 1)
        inputs.addWidget(label2, 1, 0, 1, 1)
        inputs.addWidget(self.choice2, 1, 1, 1, 1)
        inputs.addWidget(who2, 1, 2, 1, 1)
        inputs.addWidget(label3, 2, 0, 1, 1)
        inputs.addWidget(self.choice3, 2, 1, 1, 1)
        inputs.addWidget(who3, 2, 2, 1, 1)
        inputs.addWidget(label4, 3, 0, 1, 1)
        inputs.addWidget(self.choice4, 3, 1, 1, 1)
        inputs.addWidget(who4, 3, 2, 1, 1)
        b1 = QPushButton("OK", self.dialog_inst)
        b2 = QPushButton("Cancel", self.dialog_inst)
        b3 = QPushButton("Auto-guess", self.dialog_inst)
        b3.setToolTip("Let HallRober guess each PyVisa instrument available.")
        inputs.addWidget(b1, 4, 0, 1, 1)
        inputs.addWidget(b2, 4, 1, 1, 1)
        inputs.addWidget(b3, 4, 2, 1, 1)
        b1.clicked.connect(self.getInstruments)
        b2.clicked.connect(self.dialog_inst.close)
        b3.clicked.connect(self.auto_guess)
        frame_inst.addLayout(inputs)
        frame_inst.addWidget(self.status_label)
        self.find_config_file()
        self.dialog_inst.setLayout(frame_inst)
        self.dialog_inst.setFixedSize(600, 400)
        # Show makes the slots work as expected (was using "exec_" before :( )
        self.dialog_inst.show()

    def create_who_button(self):
        button = QPushButton(self.dialog_inst)
        button.setIcon(qApp.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        button.setToolTip("Who am I?")
        return button

    def send_signal(self):
        self.signals.isconfig.emit('Signal!')
        print("Signal sent!")

    def find_config_file(self):
        # Try to open/find existing config file. If not found, create from scratch
        if os.path.isfile("config.cfg"):
            print("Found already existing config file: config.cfg.")
            self.status_label.setText("Found existing config file.")
            self.config.read("config.cfg")
            cc_sample = self.config['DEFAULT']['currentsample']
            cc_coils = self.config['DEFAULT']['CurrentCoils']
            multi = self.config['DEFAULT']['Multimeter']
            arduino = self.config['DEFAULT']['Arduino']
            # The new combobox should already filter all repeated values
            # and None values.
            instpool = list(self.info)
            if cc_sample in instpool:
                a = instpool.index(cc_sample)
                #print("DEBUG: cc_sample from config_file in instpool ({})".format(a))
                self.choice2.setCurrentIndex(a)
            if cc_coils in instpool:
                a = instpool.index(cc_coils)
                #print("DEBUG: cc_coils from config_file in instpool ({})".format(a))
                self.choice3.setCurrentIndex(a)
            if multi in instpool:
                a = instpool.index(multi)
                #print("DEBUG: multimeter from config_file in instpool ({})".format(a))
                self.choice1.setCurrentIndex(a)
            if arduino in instpool:
                a = instpool.index(arduino)
                #print("DEBUG: arduino from config_file in instpool ({})".format(a))
                self.choice4.setCurrentIndex(a)
        else:
            self.status_label.setText("No config file found. Creating a new one.")
            self.config['DEFAULT'] = {'currentsample': '',
                                      'currentcoils': '',
                                      'multimeter': '',
                                      'arduino': '',
                                      'motor_position': '0',
                                      }
            with open('config.cfg', 'w') as file:
                self.config.write(file)

    def auto_guess(self):
        # We get the "IDN?" strings from each instrument and guess
        # which instrument it actually is.
        # self.info is the list of instruments. We will open each and run regex
        # Patters should have inst manuf occurrence + model number
        if len(self.info) < 3:
            self.less_than_three_inst_warn()
            return 1
        pattern_ccsource = re.compile("MODEL 622")
        pattern_multimeter = re.compile("MODEL 2010")
        #pattern_agilent = re.compile("(?=.*Agilent)(?=.*6221)")
        pattern_notInst = re.compile("ttyS0")
        pattern_hcsource = re.compile("Model 2260B-30-36")
        #pattern_hcsource = re.compile("SPD3303")

        for ind, item in enumerate(self.ports):
            #print('{} and {}'.format(ind, item))
            port_name = item.device
            if pattern_notInst.search(port_name) is not None:
                print("{} probably not an instrument. Pass.".format(item))
                pass
            elif self.arduino_PID in item.hwid:
                print("Arduino found at {}".format(port_name))
                self.choice4.setCurrentIndex(ind)
            else:
                # if it's not an arduino, we open the instrument and ask for its idn.
                ins = self.rm.open_resource('ASRL/'+ port_name)
                print("Open resource {}".format(item))
                ins.write('*IDN?')
                sleep(1)
                st = str(ins.read_raw())
                print("IDN output for instrument: {}".format(st))
                if pattern_hcsource.search(st, re.IGNORECASE) is not None:
                    print("Current source for HCoils is {}".format(item))
                    self.choice3.setCurrentIndex(ind)
                elif pattern_multimeter.search(st, re.IGNORECASE) is not None:
                    print("Multimeter is {}".format(item))
                    self.choice1.setCurrentIndex(ind)
                elif pattern_ccsource.search(st, re.IGNORECASE) is not None:
                    print("Current source for sample is {}".format(item))
                    self.choice2.setCurrentIndex(ind)
                else:
                    print("ERROR: Couldn't match the instrument's identity ({}) with any recognized "
                         "instruments.".format(st))

    def getInstruments(self):
        # First, we check that we actually have four instruments selected.
        # DEBUG: len(self.info) > 3:
        # Change to < 3 when ready to use Pyvisa!!!!!!
        if len(self.info) < 3:
            self.less_than_three_inst_warn()
            return
        # If we have four instruments as needed, we proceed to check if each one
        # has been selected only once.
        inst1 = self.choice1.currentText()
        inst2 = self.choice2.currentText()
        inst3 = self.choice3.currentText()
        inst4 = self.choice4.currentText()
        myset = set([inst1, inst2, inst3, inst4])
        if len(myset) == len([inst1, inst2, inst3, inst4]):
            # Return these values to use on the mainWindow.
            # We define attributes for the initInst class for each instr
            # after this condition is met.
            # We don't do it before to avoid passing wrong addresses
            # of instruments to MainWindow.
            # Write this LIST with the names of each instrument to use afterwards on the thread.
            # Cambiamos aca la dir del arduino para poder abrirlo luego.
            # La guardamos sin modificar en el config file.
            self.config['DEFAULT']['arduino'] = inst4
            inst4 = inst4.removeprefix('ASRL')
            inst4 = inst4.removesuffix('::INSTR')
            self.instrument_list = [inst1, inst2, inst3, inst4]
            # Write new config file parameters
            self.config['DEFAULT']['multimeter'] = inst1
            self.config['DEFAULT']['currentsample'] = inst2
            self.config['DEFAULT']['currentcoils'] = inst3

            with open('config.cfg', 'w') as file:
                self.config.write(file)
            # Close pyvisa resource manager.
            self.rm.close()
            # Emit closing signal
            self.send_signal()
            self.dialog_inst.accept()
        else:
            warn = QMessageBox()
            warn.setWindowTitle('Error')
            ico = os.path.join(os.path.dirname(__file__), "icons/laika.png")
            pixmap = QPixmap(ico).scaledToHeight(64,
                                                 Qt.SmoothTransformation)
            warn.setIconPixmap(pixmap)
            warn.setText('Two or more instruments have been selected for the\n'
                         'same function, or some instruments may not have been\n'
                         'selected. Please correct mistakes and try again.'
                         )
            warn.setStandardButtons(QMessageBox.Ok)
            warn.buttonClicked.connect(warn.close)
            warn.exec_()

    def less_than_three_inst_warn(self):
        # This opens a warning window telling the user that less than 3 instruments
        # are connected to the computer.
        print("Found less than 3 instruments connected to computer."
              "Check your connections and try again.")
        message = QMessageBox()
        ico = os.path.join(os.path.dirname(__file__), "icons/laika.png")
        pixmap = QPixmap(ico).scaledToHeight(128,
                                             Qt.SmoothTransformation)
        message.setIconPixmap(pixmap)
        message.setWindowTitle("Error")
        message.setText("Found less than 3 instruments connected to computer.\n "
                        "Check your connections and try again.")
        message.setStandardButtons(QMessageBox.Ok)
        message.buttonClicked.connect(message.close)
        message.exec_()
        