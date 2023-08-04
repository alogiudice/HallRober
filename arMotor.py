# class ArduinoM, for controlling the motor using an arduino.

import pyfirmata2 as f
import StepperLib as ar
from time import sleep

class ArduinoM:
    def __init__(self, stri, pin_1, pin_2, pin_3, pin_4):
        self.board = f.Arduino(stri)
        self.reader = f.util.Iterator(self.board)
        self.reader.start()
        self.pin_1 = self.board.get_pin('d:%s:o' % (pin_1))
        self.pin_2 = self.board.get_pin('d:%s:o' % (pin_2))
        self.pin_3 = self.board.get_pin('d:%s:o' % (pin_3))
        self.pin_4 = self.board.get_pin('d:%s:o' % (pin_4))
        self.steps_moved = 0

    def step(self, a, b, c, d, delay):
        self.pin_1.write(a)
        self.pin_2.write(b)
        self.pin_3.write(c)
        self.pin_4.write(d)
        sleep(delay)

    def move_new(self, num_step, delay):
        i = 0
        if num_step > 0:
            while i < num_step:
                self.step(1, 0, 0, 0, delay)
                self.step(1, 1, 0, 0, delay)
                self.step(0, 1, 0, 0, delay)
                self.step(0, 1, 1, 0, delay)
                self.step(0, 0, 1, 0, delay)
                self.step(0, 0, 1, 1, delay)
                self.step(0, 0, 0, 1, delay)
                self.step(1, 0, 0, 1, delay)
                i += 1
            self.steps_moved += num_step

        elif num_step < 0:
            while i < abs(num_step):
                self.step(1, 0, 0, 1, delay)
                self.step(0, 0, 0, 1, delay)
                self.step(0, 0, 1, 1, delay)
                self.step(0, 0, 1, 0, delay)
                self.step(0, 1, 1, 0, delay)
                self.step(0, 1, 0, 0, delay)
                self.step(1, 1, 0, 0, delay)
                self.step(1, 0, 0, 0, delay)
                i += 1
            self.steps_moved -= num_step
        else:
            pass

    def steps_to_angle(self, steps):
        # steps to angle conversion
        # El motor 28byj-48 tiene 512 pasos por vuelta.
        angle = steps * 360 / 512
        return round(angle)

    def angle_to_steps(self, angle):
        step = angle * (512) / 360
        return round(step)
