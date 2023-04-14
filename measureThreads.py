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
    #This thread will create a random number every 2 seconds and emit that value.
    # It is just to test threads :)
    def __init__(self, var1, var2, var3, var4):
        super(AngleThread, self).__init__()
        self.signals = WorkerSignals()
        print("Worker thread started (Angle measurement)")
        self.angle = var1
        self.field = var2
        self.current = var3
        self.number_meas = var4
        self.running = True
        print("From Worker: Angle values to be swept: {}".format(self.angle))
        print("From Worker: Applied field: {} G".format(self.field))
        print("From Worker: Applied current: {} um".format(self.current))
        print("From Worker: Number of measurements: {}".format(self.number_meas))
        print("From Worker: MEASUREMENT START (Angle sweep)")

    @pyqtSlot()
    def run(self):
        for n in self.angle:
            if self.running:
                # Set the angle with the motor and then perform a read form multimeter
                self.y = randint(1,10)
                sleep(2)
                # We emit a signal from this thread with the y value.
                self.signals.result.emit([n, self.y])
                self.signals.progress.emit(n)
            else:
                self.signals.finished.emit()
                return
        # When finished, emit "finished" signal
        self.signals.finished.emit()
        self.running = False

    def finish_run(self):
        self.running = False
        print("Changed running to: {}".format(self.running))

    def true_run(self):
        self.rm = pyvisa.ResourceManager('@py')
        self.multimeter = inst.Keithley2010(self.rm, 'NAME1')
        self.kcurrent = inst.Keithley6221(self.rm, 'NAME2')
        self.agilent = inst.FuenteAgilent(self.rm, 'NAME3')
        self.armot = motor.ArduinoM('NAME4')

        self.kcurrent.set_current(self.current)
        self.agilent.set_current(inst.field_to_voltage(self.field))
        for angle in self.angle:
            self.armot.set_angle(angle)
            mean, std = inst.mean_voltage(self.number_meas, self.multimeter)
            self.signals.result.emit([angle, mean, std])
        self.signals.finished.emit()


class FieldThread(QRunnable):
    #This thread will create a random number every 2 seconds and emit that value.
    # It is just to test threads :)
    def __init__(self, var1, var2, var3, var4, var5):
        super(FieldThread, self).__init__()
        self.signals = WorkerSignals()
        print("Worker thread started (Field measurement)")
        self.field = var1
        self.current = float(var2) * (10**-6) #en microamps
        self.angle = float(var3)
        self.num_meas = int(var4)
        self.instrument_list = var5
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
        #self.armot = motor.ArduinoM(self.rm, self.instrument_list[3])
        # Set angle and sample current
        #self.armot.set_angle(self.angle)
        self.kcurrent.set_current(self.current)
        self.kcurrent.current_on()
        for field in self.field:
            if self.running:
               self.agilent.set_voltage(1, inst.field_to_voltage(field))
               mean, std = inst.mean_voltage(self.num_meas, self.multimeter)
               self.signals.result.emit([field, mean, std])
            else:
                self.agilent.channel_1_off()
                self.kcurrent.current_off()
                self.rm.close()
                self.signals.finished.emit()
                return
        # Al terminar, cerramos rm y emitimos señal.
        self.kcurrent.current_off()
        self.rm.close()
        self.signals.finished.emit()
        self.running = False

    def finish_run(self):
        self.running = False
        print("Changed running to: {}".format(self.running))
