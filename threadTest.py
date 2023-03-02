from random import randint
from time import sleep
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def execute_this_fn(progress_callback):
    for n in range(0, 5):
        sleep(1)
        progress_callback.emit(n * 100 / 4)
    return "Done."

def thread_complete:
    print("THREAD COMPLETE!")

def thread_function_test:
    var1 = [1,2,3,4,5]
    var2 = 1.5
    var3 = 5
    worker = TestThread(execute_this_fn(var1, var2, var3))
    worker.signals.result.connect(test)
    worker.signals.finished.connect(thread_complete)
    
def test(a):
    print(a)

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    result2 = pyqtSignal(object)

class TestThread(QRunnable):
    #This thread will create a random number every 2 seconds and emit that value.
    # It is just to test threads :)
    def __init__(self, fn, var1, var2, var3):
        super(TestThread, self).__init__()
        self.signals = WorkerSignals()
        # We call a function (fn) that will send a signal while the thread
        # is processing.
        self.fn = fn
        self.angle = var1
        self.angle2 = var2
        self.angle3 = var3
        print("var1 is: {}".format(self.angle))
        print("var2 is: {}".format(self.angle2))
        print("var3 is: {}".format(self.angle3))
        #.kwargs['progress_callback'] = self.signals.result

    @pyqtSlot()
    def run(self):
        for n in range(0,10):
            self.y = randint(1,10)
            sleep(2)
            # We emit a signal from this thread with the y value.
            self.signals.result.emit(self.y)
        # When finished, emit "finished" signal
        self.signals.finished.emit()

class MyCustomWidget(QWidget):

    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,100)
        button = QPushButton("Start", self)
        layout.addWidget(self.progressBar)
        layout.addWidget(button)

        button.clicked.connect(self.onStart)
        ##############################################################
        #and pass your argumetn to it's constructor here
        self.myLongTask = TaskThread(myvar=myargument)
        ##############################################################
        self.myLongTask.notifyProgress.connect(self.onProgress)




