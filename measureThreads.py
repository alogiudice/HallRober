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
        while self.running:
            for n in self.angle:
                # Set the angle with the motor and then perform a read form multimeter
                self.y = randint(1,10)
                sleep(2)
                # We emit a signal from this thread with the y value.
                self.signals.result.emit(self.y)
                self.signals.progress.emit(n)
            # When finished, emit "finished" signal
            self.signals.finished.emit()
            self.running = False

    #@pyqtSlot()
    def finish_run(self):
        self.running = False
        print("Changed running to: {}".format(self.running))
        self.signals.finished.emit()

    def true_run(self):
        self.rm = pyvisa.ResourceManager('@py')
        self.multimeter = inst.Keithley2010(self.rm, 'NAME')
        self.kcurrent = inst.Keithley6221(self.rm, 'NAME')
        self.agilent = inst.FuenteAgilent(self.rm, 'NAME')
        self.armot = motor.ArduinoM('NAME')

        self.kcurrent.set_current(self.current)
        self.agilent.set_current(inst.field_to_voltage(self.field))
        for angle in self.angle:
            self.armot.set_angle(angle)
            mean, std = inst.mean_voltage(self.number_meas, self.multimeter)
            self.signals.result.emit(mean)
            self.signals.result2.emit(std)
        self.signals.finished.emit()


class FieldThread(QRunnable):
    #This thread will create a random number every 2 seconds and emit that value.
    # It is just to test threads :)
    def __init__(self, var1, var2, var3):
        super(FieldThread, self).__init__()
        self.signals = WorkerSignals()
        print("Worker thread started (Field measurement)")
        self.field = var1
        self.angle = var2
        self.current = var3
        print("From Worker: Field values to be swept: {}".format(self.angle))
        print("From Worker: Sample Angle: {}".format(self.field))
        print("From Worker: Applied current: {}".format(self.current))
        print("From Worker: MEASUREMENT START (Field sweep)")

    @pyqtSlot()
    def run(self):
        for n in range(0,10):
            # Set the angle with the motor and then perform a read form multimeter
            self.y = randint(1,10)
            sleep(2)
            # We emit a signal from this thread with the y value.
            self.signals.result.emit(self.y)
        # When finished, emit "finished" signal
        self.signals.finished.emit()

    @pyqtSlot()
    def end(self):
        self.quit()
