import equipos as inst
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from random import randint
from time import sleep

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    result2 = pyqtSignal(object)

class AngleThread(QRunnable):
    #This thread will create a random number every 2 seconds and emit that value.
    # It is just to test threads :)
    def __init__(self, var1, var2, var3):
        super(AngleThread, self).__init__()
        self.signals = WorkerSignals()
        print("Worker thread started (Angle measurement)")
        self.angle = var1
        self.field = var2
        self.current = var3
        print("From Worker: Angle values to be swept: {}".format(self.angle))
        print("From Worker: Applied field: {} G".format(self.field))
        print("From Worker: Applied current: {} um".format(self.current))
        print("From Worker: MEASUREMENT START (Angle sweep)")

    @pyqtSlot()
    def run(self):
        for n in self.angle:
            # Set the angle with the motor and then perform a read form multimeter
            self.y = randint(1,10)
            sleep(2)
            # We emit a signal from this thread with the y value.
            self.signals.result.emit(self.y)
            self.signals.progress.emit(n)
        # When finished, emit "finished" signal
        self.signals.finished.emit()

    @pyqtSlot()
    def end(self):
        self.quit()

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
