import equipos as inst
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from random import randint
from time import sleep
import pyvisa
import arMotor as motor


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    result2 = pyqtSignal(object)

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
        self.armot = motor.ArduinoM(self.arduino_dir, 9, 10, 11, 12)
        # Pasamos a steps los valores angulares
        steps_final = self.armot.angle_to_steps(self.angle_list[1])
        steps_inic = self.armot.angle_to_steps(self.angle_list[0])
        # El saltito entre el cual vamos a medir.
        num_steps = self.armot.angle_to_steps(self.angle_list[2])
        self.kcurrent.set_current(self.current)
        self.kcurrent.current_on()
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
    # This thread will create a random number every 2 seconds and emit that value.
    # It is just to test threads :)
    def __init__(self, var1, var2, var3, var4, var5):
        super(FieldThread, self).__init__()
        self.signals = WorkerSignals()
        print("Worker thread started (Field measurement)")
        self.field = var1
        self.current = float(var2) * (10**-6) # en microamps
        self.angle = float(var3)
        self.num_meas = int(var4)
        self.instrument_list = var5
        self.instrument_list[3].replace('ASRL', '')
        self.instrument_list[3].replace('::INSTR', '')
        self.running = True
        print("From FIELDWORKER: Field values to be swept: {}".format(self.field))
        print("From FIELDWORKER: Sample Angle: {}".format(self.angle))
        print("From FIELDWORKER: Applied current: {}".format(self.current))
        print("From FIELDWORKER: Number of measurements per field: {}".format(self.num_meas))
        print("From FIELDWORKER: List of instruments: {}".format(self.instrument_list))
        print("From FIELDWORKER: MEASUREMENT START (Field sweep)")

    @pyqtSlot()
    def run(self):
        self.rm = pyvisa.ResourceManager('@py')
        self.multimeter = inst.Keithley2010(self.rm, self.instrument_list[0])
        self.kcurrent = inst.Keithley6221(self.rm, self.instrument_list[1])
        #self.agilent = inst.FuenteAgilent(self.rm, self.instrument_list[2])
        self.agilent = inst.Fuente_Siglent(self.rm, self.instrument_list[2])
        # Usamos los pines 9, 10, 11, 12 del arduino.
        self.armot = motor.ArduinoM(self.instrument_list[3], 9, 10, 11, 12)
        # Set angle and sample current
        # delay in one total step = 0.4 secs
        self.armot.move_new(self.armot.angle_to_steps(self.angle), 0.05)
        self.kcurrent.set_current(self.current)
        self.kcurrent.current_on()
        for field in self.field:
            if self.running:
               self.agilent.set_voltage(1, inst.field_to_voltage(field))
               self.agilent.channel_1_on()
               mean, std = inst.mean_voltage(self.num_meas, self.multimeter)
               self.signals.result2.emit('Measuring at field {} G'.format(self.field))
               self.signals.result.emit([field, mean, std])

            else:
                self.agilent.channel_1_off()
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
