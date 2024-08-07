#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:09:03 2022

@author: agostina
"""

## Instrumentos comunes del laboratorio

from time import sleep
import numpy as np
import pyvisa
from pyvisa.constants import StopBits, Parity

class Keithley6221:
    # Fuente de Corriente Keithley   
    def __init__(self, rm, name):
        self.inst = rm.open_resource('{}'.format(name))
        # Setting baud, terminator and flow control.
        self.inst.write('SYST:COMM:SER:BAUD 9600')
        sleep(1)
        self.inst.write('SYST:COMM:SER:TERM LF')
        sleep(1)
        self.inst.write('SYST:COMM:SER:PACE OFF')
        
    def identity(self):
        self.inst.write('*IDN?\n')
        sleep(1)
        print('Hi! My name is {}'.format(self.inst.read_raw()))  
        
    def set_current(self, amps):
        self.inst.write('CURRent {}'.format(amps))
        
    def current_on(self):
        self.inst.write('OUTput ON')

    def current_off(self):
        self.inst.write('OUTput OFF')

    def set_baud(self, num=9600):
        # Sets the baud rate of the current source.
        # Default is 9600. Other options are:
        #  300, 600, 1200, 2400, 4800,
        # 9600, 19.2k, 38.4K, 57.6K, or 115.2K.

        self.inst.write('SYST:COMM:SER:BAUD {}'.format(num))

    def set_terminator(self, stri='LF'):
        # Sets terminator. Default is LF.
        # Other options are = CR, CRLF, or LFCR.
        self.inst.write('SYST:COMM:SER:TERM {}'.format(stri))

    def set_flow_control(self, stri='OFF'):
        # Sets flow control (XON or OFF)
        self.inst.write('SYST:COMM:SER:PACE {}'.format(stri))
class Fuente_Siglent:
    # Fuente Siglent para las bobinas    
    def __init__(self, rm, name):
        self.instf = rm.open_resource('{}'.format(name))
        # Modify termination character
        self.instf.write_termination = '\n'
        self.instf.read_termination = '\n'
        
    def identity(self):
        self.instf.write('*IDN?')
        sleep(1)
        print('Hi! My name is {}'.format(self.instf.read_raw()))
        
    def channel_2_on(self):
        self.instf.write('OUTP CH2,ON')

    def channel_2_off(self):
        self.instf.write('OUTP CH2,OFF')

    def channel_1_on(self):
        self.instf.write('OUTP CH1,ON')

    def channel_1_off(self):
        self.instf.write('OUTP CH1,OFF')

    def set_channel(self, num):
        self.instf.write('INSTrument CH{}'.format(num))
        
    def query_channel(self):
        # NO anda
        self.instf.query('INSTrument?')
        
    def set_voltage(self, channel, num):
        if num < 0:
            num = abs(num)
        string = 'CH{}:VOLTage {}'.format(channel, num)
        self.instf.write(string)
        
    def set_current(self, channel, num):
        string = 'CH{}:CURRent {}'.format(channel, num)
        self.instf.write(string)
        
    def channel_voltage(self, channel):
        test = self.instf.query('CH{}:VOLT?'.format(channel))
        return test
    
    def channel_current(self, channel):
        test = self.instf.query('CH{}:CURRent?'.format(channel))
        return test
    
class FuenteAgilent:
    # Fuente DC Agilent
    def __init__(self, rm, name):
        self.instf = rm.open_resource('{}'.format(name))
        self.instf.write_termination='\n'
        self.instf.read_termination='\n'
        
    def set_voltage(self, num):
        # in Volts
        self.instf.write('VOLT {}'.format(num))
    
    def set_current(self, num):
        # in A
        self.instf.write('CURR {}'.format(num))
        
    def read_current(self):
        return self.instf.query('MEAS:CURR?')
    
    def ps_output(self, st):
        #Puede ser ON u OFF
        self.instf.write('OUTPut {}'.format(st))

class Keithley2260:
    # Fuente Keithley chiquita
    def __init__(self, rm, name):
        self.inst = rm.open_resource('{}'.format(name))
    def identity(self):
        self.inst.write('*IDN?\n')
        sleep(1)
        print('Hi! My name is {}'.format(self.inst.read_raw()))
    def set_voltage(self, voltage):
        self.inst.write('SOUR:VOLT:LEV:IMM:AMPL {}'.format(voltage))

    def query_voltage(self):
        self.inst.write('SOUR:VOLT:LEV:IMM:AMPL?')
        sleep(0.5)
        stri = self.inst.read_raw()
        return stri

    def set_current(self, current):
        self.inst.write('SOUR:CURR:LEV:IMM:AMPL {}'.format(current))
    def query_current(self):
        self.inst.write('SOUR:CURR:LEV:IMM:AMPL?')
        sleep(0.5)
        stri = self.inst.read_raw()
        return stri
    def output_on(self):
        self.inst.write('OUTP:STAT:IMM 1')

    def output_off(self):
        self.inst.write('OUTP:STAT:IMM 0')
    
class Keithley2010:
    #Multímetro Keithley    
    def __init__(self, rm, name):
        self.inst = rm.open_resource('{}'.format(name))
        #'ASRL/dev/ttyUSB0::INSTR'
        
    def identity(self):
        self.inst.write('*IDN?\n')
        sleep(1)
        print('Hi! My name is {}'.format(self.inst.read_raw()))
        
    def read(self):
        test = self.inst.query(':FETCh?\n')
        #wait one second before reading output. 
        #ime.sleep(1)
        #test = self.inst.read_bytes(1)
        return test
    
    def set_rate(self, rate):
        # Integration rate
        # Values between 0.1 (fastest) and 10 (slowest)
        self.inst.write(':VOLT:NPLCycles {}'.format(rate))
        
class Gaussimetro:
    # Ahora el gaussimetro LakeShore 455 anda correctamente al especificar los valores de data bits, flowcontrol,
    # parity y el stop bit. :)
    # Estos valores estan en el manual del dispositivo.
    def __init__(self, rm, name):
        self.inst = rm.open_resource('{}'.format(name), baud_rate=9600, data_bits=7, flow_control=2,
                                     parity=Parity.odd, stop_bits=StopBits.one)
        
    def identity(self):
        self.inst.write('*IDN?')
        sleep(1)
        print('Hi! My name is {}'.format(self.inst.read_raw()))
        
    def read(self):
        field = self.inst.query('RDGFIELD?')
        sleep(1)
        return field


## Funciones auxiliares para las mediciones ##

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def mean_voltage(sample_num, multi):
    voltage = []
    i = 0
    for i in range(0, sample_num):
        sleep(0.1)
        value = multi.read()
        value.replace('\n', '')
        voltage.append(float(value))
        i += 1
    mean = np.mean(voltage)
    std = np.std(voltage) / np.sqrt(len(voltage))
    return mean, std


def field_to_voltage(field):
    # Using last calibration.
    volt = truncate(((field + 0.0497) / 3.286), decimals=3)
    volt = ((field + 0.0497) / 3.286)
    return volt

def field_to_current(field):
    # Using last calibration.
    current = (field + 0.0232) / 0.1742
    current /= 1000
    return current

def current_sweep(initial, final, num_measures):
    # Devuelve las corrientes a escanear para lograr x cantidad de campos
    # entre un campo inicial y uno final.
    fields = np.linspace(initial, final, num=num_measures)
    fields_c = [field_to_current(value) for value in fields]
    return fields_c