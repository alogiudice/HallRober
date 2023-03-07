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






