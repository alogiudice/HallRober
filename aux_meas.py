#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 12:37:41 2021

@author: agostina
"""

import numpy as np
import pyvisa
import time
#import os
import matplotlib.pyplot as plt
import pandas as pd



    

        

rm = pyvisa.ResourceManager('@py')

kei = FuenteKeithley(rm, 2)
multi = Multimeter(rm, 1)
fuente = Fuente_Siglent(rm, 3)

sample_name = 'CoFe40nm_SC_Ag'
field_orientation = 'para'
maxfield = '200G'
ibias = 5e-4 # 0.5 mA
measure = '{}_0,5mA_{}_{}_5segwtime'.format(sample_name, field_orientation, maxfield)

multi.set_rate(5)
# Aplico corriente bias
kei.set_current(ibias)
kei.current_on()


fields1 = np.arange(200, 100, -20)
fields2 = np.arange(100, 50, -10)
fields3 = np.arange(50, 10, -5)
fields4 = np.arange(10, 1, -1)
fields = np.concatenate((fields1, fields2, fields3, fields4))
field_reverse = np.flip(fields)
voltages = []
voltstd = []
times = []

# Arranco con 35G
#Subimos de a poco
'''
fuente.set_voltage(1,(field_to_voltage(50)/2))
time.sleep(5)
fuente.channel_1_on()
time.sleep(3)
fuente.set_voltage(1,(field_to_voltage(70)/2))
time.sleep(3)
fuente.set_voltage(1,(field_to_voltage(90)/2))
time.sleep(3)
fuente.set_voltage(1,(field_to_voltage(100)/2))
time.sleep(3)
fuente.set_voltage(1,(field_to_voltage(130)/2))
time.sleep(3)
fuente.set_voltage(1,(field_to_voltage(160)/2))
time.sleep(3)
fuente.set_voltage(1,(field_to_voltage(190)/2))
time.sleep(3)
fuente.set_voltage(1,(field_to_voltage(200)/2))
'''
fuente.set_current(1,(field_to_current(50)))
time.sleep(5)
fuente.channel_1_on()
time.sleep(3)
fuente.set_current(1,(field_to_current(70)))
time.sleep(3)
fuente.set_current(1,(field_to_current(90))
time.sleep(3)
fuente.set_current(1,(field_to_current(100)/2))
time.sleep(3)
fuente.set_current(1,(field_to_current(130)/2))
time.sleep(3)
fuente.set_current(1,(field_to_current(160)/2))
time.sleep(3)
fuente.set_current(1,(field_to_current(190)/2))
time.sleep(3)
fuente.set_current(1,(field_to_current(200)))

initial_time = time.time()
for field in fields:
    fuente.set_current(1,(field_to_current(field))/2)
    time.sleep(5)
    mean,std = mean_voltage(50)
    times.append(time.time() - initial_time)
    voltages.append(mean)
    voltstd.append(std)
    
## Campos reversos
# DAR VUELTA LOS CABLES
input('DAR VUELTA LOS CABLES DE LA FUENTE (+ -- -)')
    ##########
    
for field in field_reverse:
    fuente.set_voltage(1,(field_to_voltage(field)/2))
    time.sleep(5)
    mean,std = mean_voltage(50)
    times.append(time.time() - initial_time)
    voltages.append(mean)
    voltstd.append(std)
    
fuente.set_voltage(1,(field_to_voltage(130)/2))
    
#Curva de vuelta (histeresis)
    ##################################################################
for field in fields:
    fuente.set_voltage(1,(field_to_voltage(field)/2))
    time.sleep(5)
    mean,std = mean_voltage(50)
    times.append(time.time() - initial_time)
    voltages.append(mean)
    voltstd.append(std)
    
    
### DAR VUELTA LOS CABLES
input('DAR VUELTA LOS CABLES DE LA FUENTE (- -- +)')
for field in field_reverse:
    fuente.set_voltage(1,(field_to_voltage(field)/2))
    time.sleep(5)
    mean,std = mean_voltage(50)
    times.append(time.time() - initial_time)
    voltages.append(mean)
    voltstd.append(std)
    
                                                                                                                                                                                                                                                                       


## Grafico los dos ciclos superpuestos.
## Guardo los datos

## field_map es un barrido desde +Hsat a -Hsat.
field_map = np.append(fields, (-1)*field_reverse)
field_map_reverse = np.flip(field_map)
field_total = np.append(field_map, field_map_reverse)      
                                   
np.save(measure+'.npy', np.array([times, field_total, voltages, voltstd]))    

a = np.stack((times, field_total, voltages, voltstd), axis=-1)
test = pd.DataFrame(a, columns=['time', 'field [G]', 'voltage', 'voltstd'])
test.to_csv(measure +'.csv')

# Grafico los dos ciclos superpuestos:  

test = np.split(np.array(voltages), 2)
stdev = np.split(np.array(voltstd), 2)

fig = plt.figure()
fig.clear()
ax = fig.add_subplot(111)
ax.set_ylabel('Voltage [V]')
ax.set_xlabel('Field [G]')
#ax.set_title(measure)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
ax.grid()
ax.plot(field_map, test[0], marker='.', color='red', label='first')     
ax.plot(field_map_reverse, test[1], marker='.', color='blue', label='reverse')
ax.legend(loc='upper left')
fig.canvas.draw()

fig2 = plt.figure()
fig2.clear()
ax2 = fig2.add_subplot(111)
ax2.set_ylabel('Voltage [V]')
ax2.set_xlabel('Field [G]')
ax2.set_title(measure)  
ax2.grid()
ax2.errorbar(field_map[37:52], test[0][37:52], yerr=stdev[0][37:52], marker='o', color='red', label='First')
ax2.errorbar(field_map_reverse[37:52], test[1][37:52], yerr=stdev[1][37:52], marker='o', color='blue', label='Second')
ax2.legend()





## Vamos a: on channel 2 fuente; ir a 35G; medir V; ir bajando en un loop.




######


def initialize_instruments(self):
    # List the different instruments connected to the PC.
    self.rm = pyvisa.ResourceManager('@py')
    self.info = self.rm.list_resources()
    self.dialog_inst = QDialog(self)
    self.dialog_inst.setWindowTitle("Instruments")
    frame_inst = QVBoxLayout(self.dialog_inst)
    inputs = QGridLayout(self.dialog_inst)
    text_inst_output = QTextBrowser(self.dialog_inst)
    label1 = QLabel(self.dialog_inst)
    label1.setText('As multimeter, use:')
    choice1 = QComboBox(self.dialog_inst)
    label2 = QLabel(self.dialog_inst)
    label2.setText('As current source for sample, use:')
    choice2 = QComboBox(self.dialog_inst)
    label3 = QLabel(self.dialog_inst)
    label3.setText('As current source for coils, use:')
    choice3 = QComboBox(self.dialog_inst)
    label4 = QLabel(self.dialog_inst)
    label4.setText('As an Arduino for the motor, use:')
    choice4 = QComboBox(self.dialog_inst)
    i = 1
    for item in self.info:
        text_inst_output.append('{}) dir: {}\n'.format(i, item))
        choice1.addItem(item)
        choice2.addItem(item)
        choice3.addItem(item)
        choice4.addItem(item)
        ++i
    frame_inst.addWidget(text_inst_output)
    inputs.addWidget(label1, 0, 0, 1, 1)
    inputs.addWidget(choice1, 0, 1, 1, 1)
    inputs.addWidget(label2, 1, 0, 1, 1)
    inputs.addWidget(choice2, 1, 1, 1, 1)
    inputs.addWidget(label3, 2, 0, 1, 1)
    inputs.addWidget(choice3, 2, 1, 1, 1)
    inputs.addWidget(label4, 3, 0, 1, 1)
    inputs.addWidget(choice4, 3, 1, 1, 1)
    b1 = QPushButton("OK", self.dialog_inst)
    b2 = QPushButton("Cancel", self.dialog_inst)
    inputs.addWidget(b1, 4, 0, 1, 1)
    inputs.addWidget(b2, 4, 1, 1, 1)
    b1.clicked.connect(self.getInstruments(choice1.currentText(), choice2.currentText(),
                                           choice3.currentText(), choice4.currentText()))
    b2.clicked.connect(self.dialog_inst.close)
    frame_inst.addLayout(inputs)
    self.dialog_inst.setLayout(frame_inst)
    self.dialog_inst.setFixedSize(400, 400)
    self.dialog_inst.setWindowModality(Qt.ApplicationModal)
    self.dialog_inst.exec_()


def getInstruments(self, inst1, inst2, inst3, inst4):
    # Instruments are opened with this function; no need to reopen them later
    myset = set([inst1, inst2, inst3, inst4])
    if len(myset) == len([inst1, inst2, inst3, inst4]):
        self.keithley_2010 = inst.Keithley2010(self.rm, inst1)
        self.keithley_6221 = inst.Keithley6221(self.rm, inst2)
        self.agilent = inst.FuenteAgilent(self.rm, inst3)
        # self.motor = ard.ArduinoM(inst4)
        self.dialog_inst.close()
    else:
        warn = QMessageBox()
        warn.setWindowTitle('Error')
        # ico = os.path.join(os.path.dirname(__file__), "icons/laika.png")
        # pixmap = QPixmap(ico).scaledToHeight(64,
        #                                    Qt.SmoothTransformation)
        # warn.setIconPixmap(pixmap)
        warn.setText('Two or more instruments have been selected for the\n'
                     'same function, or some instruments may not have been\n'
                     'selected. Please correct mistakes and try again.'
                     )
        warn.setStandardButtons(QMessageBox.Ok)
        warn.buttonClicked.connect(warn.close)
        warn.exec_()



