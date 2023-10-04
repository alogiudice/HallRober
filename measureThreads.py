from pyvisa import InvalidSession

import arMotor
import equipos as inst
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from random import randint
from time import sleep
import pyvisa
import arMotor as motor
import numpy as np


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    result2 = pyqtSignal(object)
    sample_saturated = pyqtSignal()

class AngleThread(QRunnable):
    def __init__(self, var1, var2, var3, var4, var5):
        super(AngleThread, self).__init__()
        self.signals = WorkerSignals()
        print("Worker thread started (Angle measurement)")
        # Angle list = [ang_inic, ang_fin, ang_steps]
        self.angle_list = var1
        self.field = var2
        self.current = var3
        self.number_meas = var4
        self.instrument_list = var5
        self.arduino_dir = self.instrument_list[3]
        self.motor_pins = [12, 11, 10, 9]
        self.relay_pins = [2, 3, 4, 5]
        print('DEBUG: ARDUINO DIR: {}'.format(self.arduino_dir))
        self.arduino_dir.replace('ASRL', '')
        self.arduino_dir.replace('::INSTR', '')
        print('DEBUG: ARDUINO DIR: {}'.format(self.arduino_dir))
        # We reformat the last string from instrument_list since the arduino needs the ttyACM dir to initialize.
        self.running = True
        print("From ANGLEWORKER: Angle values to be swept: {}".format(self.angle_list))
        print("From ANGLEWORKER: Applied field: {} G".format(self.field))
        print("From ANGLEWORKER: Applied current: {} um".format(self.current))
        print("From ANGLEWORKER: Number of measurements: {}".format(self.number_meas))
        print("From ANGLEWORKER: List of instruments: {}".format(self.instrument_list))
        print("From Worker: MEASUREMENT START (Angle sweep)")


    @pyqtSlot()
    def run(self):
        self.rm = pyvisa.ResourceManager('@py')
        self.multimeter = inst.Keithley2010(self.rm, self.instrument_list[0])
        self.kcurrent = inst.Keithley6221(self.rm, self.instrument_list[1])
        # self.agilent = inst.FuenteAgilent(self.rm, self.instrument_list[2])
        self.agilent = inst.Fuente_Siglent(self.rm, self.instrument_list[2])
        # Usamos los pines 9, 10, 11, 12 del arduino.
        self.armot = motor.ArduinoM(self.arduino_dir, self.motor_pins, self.relay_pins)
        # Pasamos a steps los valores angulares
        steps_final = self.armot.angle_to_steps(self.angle_list[1])
        steps_inic = self.armot.angle_to_steps(self.angle_list[0])
        # El saltito entre el cual vamos a medir.
        num_steps = self.armot.angle_to_steps(self.angle_list[2])
        self.kcurrent.set_current(self.current)
        self.kcurrent.current_on()
        self.armot.change_relay_config(np.sign(self.field))
        sleep(1)
        self.agilent.set_voltage(1, inst.field_to_voltage(self.field))
        self.agilent.channel_1_on()
        sleep(1)
        # Vamos al valor inicial del ang (es decir, move to init_step)
        self.armot.move_new(steps_inic, 0.05)
        while abs(self.armot.steps_moved) < abs(steps_final):
            if self.running:
                self.armot.move_new(num_steps, 0.05)
                current_angle = self.armot.steps_to_angle(self.armot.steps_moved)
                mean, std = inst.mean_voltage(self.number_meas, self.multimeter)
                self.signals.result.emit([current_angle, mean, std])
                self.signals.result2.emit('Current step: {} ({} deg)\n'.format(self.armot.steps_moved,
                                                                               current_angle))
            else:
                self.agilent.channel_1_off()
                self.kcurrent.current_off()
                self.rm.close()
                # Return to starting position
                self.signals.result2.emit('Moving motor back to start position.')
                self.armot.move_new(self.armot.steps_moved * (-1), 0.005)
                self.signals.finished.emit()
                return
        # Al terminar, cerramos rm y emitimos señal.
        self.kcurrent.current_off()
        self.agilent.channel_1_off()
        self.signals.result2.emit('Moving motor back to start position.')
        self.armot.move_new(self.armot.steps_moved * (-1), 0.005)
        self.rm.close()
        self.signals.finished.emit()
        self.running = False

    def finish_run(self):
        self.running = False
        print("Changed running to: {}".format(self.running))


class FieldThread(QRunnable):
    def __init__(self, var1, var2, var3, var4, var5):
        super(FieldThread, self).__init__()
        self.signals = WorkerSignals()
        print("Worker thread started (Field measurement)")
        self.field = var1
        self.current = var2 # en microamps
        self.angle = float(var3)
        self.num_meas = int(var4)
        self.instrument_list = var5
        self.instrument_list[3].replace('ASRL', '')
        self.instrument_list[3].replace('::INSTR', '')
        self.arduino_dir = self.instrument_list[3]
        self.motor_pins = [12, 11, 10, 9]
        self.relay_pins = [2, 3, 4, 5]
        self.running = True
        print("From FIELDWORKER: Field values to be swept: {}".format(self.field))
        print("From FIELDWORKER: Sample Angle: {}".format(self.angle))
        print("From FIELDWORKER: Applied current: {}".format(self.current))
        print("From FIELDWORKER: Number of measurements per field: {}".format(self.num_meas))
        print("From FIELDWORKER: List of instruments: {}".format(self.instrument_list))
        print("From FIELDWORKER: MEASUREMENT START (Field sweep)")

    def sign_changed(self, varr1, varr2):
        if np.sign(varr1) == np.sign(varr2):
            # NO sign change. Proceed
            return False
        elif varr2 == 0:
            return False
        else:
            return True

    @pyqtSlot()
    def run(self):
        self.rm = pyvisa.ResourceManager('@py')
        self.multimeter = inst.Keithley2010(self.rm, self.instrument_list[0])
        self.kcurrent = inst.Keithley6221(self.rm, self.instrument_list[1])
        #self.agilent = inst.FuenteAgilent(self.rm, self.instrument_list[2])
        self.agilent = inst.Fuente_Siglent(self.rm, self.instrument_list[2])
        # Usamos los pines 9, 10, 11, 12 del arduino.
        self.armot = motor.ArduinoM(self.arduino_dir, self.motor_pins, self.relay_pins)
        # Set angle and sample current
        # delay in one total step = 0.4 secs
        self.armot.move_new(self.armot.angle_to_steps(self.angle), 0.05)
        self.kcurrent.set_current(self.current)
        self.kcurrent.current_on()
        self.armot.change_relay_config(np.sign(self.field[0]))
        last_field = self.field[0]
        sleep(1)
        self.agilent.channel_1_on()
        sleep(1)
        # Armamos array ida y vuelta de los campos
        self.field_total = np.concatenate((self.field, np.flip(self.field)))
        # Setteamos la direcc del campo inicial.
        self.armot.change_relay_config(np.sign(self.field_total[0]))
        for field in self.field_total:
            if self.running:
                if self.sign_changed(field, last_field):
                    print('Changed relay config.')
                    self.armot.change_relay_config(np.sign(last_field * -1))
                self.agilent.set_voltage(1, inst.field_to_voltage(field))
                sleep(2)
                print(inst.field_to_voltage(field))
                mean, std = inst.mean_voltage(self.num_meas, self.multimeter)
                self.signals.result2.emit('Measuring at field {} G ({} Volts)'.format(field,
                                                                                      inst.field_to_voltage(field)))
                self.signals.result.emit([field, mean, std])
                last_field = field
            else:
                self.agilent.channel_1_off()
                sleep(1)
                self.kcurrent.current_off()
                # Return arduino to starting position
                self.signals.result2.emit('Moving motor back to start position.')
                self.armot.move_new(self.armot.steps_moved * (-1), 0.03)
                self.rm.close()
                self.signals.finished.emit()
                return
        # Al terminar, cerramos rm y emitimos señal.
        self.kcurrent.current_off()
        self.agilent.channel_1_off()
        self.signals.result2.emit('Moving motor back to start position.')
        self.armot.move_new(self.armot.steps_moved * (-1), 0.03)
        self.rm.close()
        self.signals.finished.emit()
        self.running = False

    def finish_run(self):
        self.running = False
        print("Changed running to: {}".format(self.running))


class SensThread(QRunnable):
    def __init__(self, app, var1, var2, var3, var4, var5, var6):
        super(SensThread, self).__init__()
        self.app = app
        self.signals = WorkerSignals()
        print("Worker thread started (Field measurement)")
        self.field = var1
        self.current = var2 # en microamps
        self.angle = float(var3)
        self.num_meas = int(var4)
        self.instrument_list = var5
        self.saturation_f = var6
        self.instrument_list[3].replace('ASRL', '')
        self.instrument_list[3].replace('::INSTR', '')
        self.arduino_dir = self.instrument_list[3]
        self.motor_pins = [12, 11, 10, 9]
        self.relay_pins = [2, 3, 4, 5]
        self.running = True
        self.rm = pyvisa.ResourceManager('@py')
        self.multimeter = inst.Keithley2010(self.rm, self.instrument_list[0])
        self.kcurrent = inst.Keithley6221(self.rm, self.instrument_list[1])
        self.agilent = inst.Fuente_Siglent(self.rm, self.instrument_list[2])
        self.armot = motor.ArduinoM(self.arduino_dir, self.motor_pins, self.relay_pins)
        print("From SENSWORKER: Saturation Field: {} G".format(self.saturation_f))
        print("From SENSWORKER: Field values to be swept: {}".format(self.field))
        print("From SENSWORKER: Sample Angle: {}".format(self.angle))
        print("From SENSWORKER: Applied current: {} A".format(self.current))
        print("From SENSWORKER: Number of measurements per field: {}".format(self.num_meas))
        print("From SENSWORKER: List of instruments: {}".format(self.instrument_list))
        print("From SENSWORKER: MEASUREMENT START (Sensitivity sweep)")

    @pyqtSlot()
    def run(self):
        # Set angle and sample current
        # delay in one total step = 0.4 secs
        self.armot.move_new(self.armot.angle_to_steps(self.angle), 0.05)
        self.armot.change_relay_config(np.sign(self.saturation_f))
        self.multimeter.set_rate(5)
        sleep(1)
        self.agilent.set_voltage(1, inst.field_to_voltage(self.saturation_f))
        print("Voltage for sample saturation: {} V".format(inst.field_to_voltage(self.saturation_f)))
        sleep(1)
        self.agilent.channel_1_on()
        sleep(10)
        self.agilent.channel_1_off()
        sleep(1)
        self.app.showMessage_saturation.emit()
        while not self.app.sample_saturated:
            sleep(0.1)
        # Fuente agilent alimenta a la muestra
        print("FROM SENS THREAD: SAMPLE SATURATED. MEASUREMENT START")
        self.agilent.set_channel(2)
        sleep(1)
        self.agilent.set_voltage(2, 2.5)
        sleep(1)
        self.agilent.set_current(2, self.current)
        sleep(1)
        self.agilent.channel_2_on()
        sleep(1)
        # Relay in forward mode for keithley source
        self.armot.change_relay_config(1)
        sleep(1)
        self.kcurrent.set_current(inst.field_to_current(self.field[0]))
        self.kcurrent.current_on()
        #test
        for field in self.field:
            if self.running:
                self.kcurrent.set_current(inst.field_to_current(field))
                sleep(5)
                mean, std = inst.mean_voltage(self.num_meas, self.multimeter)
                self.signals.result2.emit('Measuring at field {} G ({} amps)'.format(field,
                                                                                     inst.field_to_current(field)))
                self.signals.result.emit([field, mean, std])
            else:
                print('Running is {}'.format(self.running))
                self.agilent.channel_2_off()
                sleep(1)
                self.kcurrent.current_off()
                # Return arduino to starting position
                self.signals.result2.emit('Moving motor back to start position.')
                self.armot.move_new(self.armot.steps_moved * (-1), 0.03)
                self.rm.close()
                self.signals.finished.emit()
                return
        # Al terminar, cerramos rm y emitimos señal.
        self.kcurrent.current_off()
        self.agilent.channel_2_off()
        self.signals.result2.emit('Moving motor back to start position.')
        self.armot.move_new(self.armot.steps_moved * (-1), 0.03)
        self.rm.close()
        self.signals.finished.emit()
        self.running = False
        self.app.sample_saturated = False

    def finish_run(self):
        self.running = False
        print("Changed running to: {}".format(self.running))

class SampleReset(QRunnable):
    def __init__(self, app, var1, var2, var3):
        self.field = var1
        self.app = app
        self.signals = WorkerSignals()
        self.stabilization_time = var3
        self.rm = pyvisa.ResourceManager('@py')
        self.instrument_list = var2
        self.motor_pins = [12, 11, 10, 9]
        self.relay_pins = [2, 3, 4, 5]
        self.siglent = inst.Fuente_Siglent(self.rm, self.instrument_list[2])
        self.arduino_dir = self.instrument_list[3]
        self.arduino = arMotor.ArduinoM(self.rm, self.arduino_dir, self.motor_pins, self.relay_pins)

    @pyqtSlot()
    def run(self):
        print('FROM SAMPLERESET: SET ANGLE TO 90DEG')
        self.arduino.move_new(self.arduino.angle_to_steps(90))
        print('FROM SAMPLERESET: SATURATE SAMPLE WITH {} G'.format(self.field))
        self.siglent.set_voltage(1, inst.field_to_voltage(self.field))
        sleep(1)
        self.siglent.channel_1_on()
        print('FROM SAMPLERESET: STABILIZATION TIME - {} SECS'.format(self.stabilization_time))
        sleep(self.stabilization_time)
        print('FROM SAMPLERESET: STABILIZATION COMPLETED.')
        self.siglent.channel_1_off()
        sleep(1)

