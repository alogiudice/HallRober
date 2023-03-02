# class ArduinoM, for controlling the motor using an arduino.

import pyfirmata2 as f
import StepperLib

class ArduinoM:
    def __init__(self, stri):
        self.board = f.Arduino(stri)
        reader = f.util.Iterator(self.board)
        reader.start()
        self.motor = StepperLib.Stepper(2038, self.board, reader, 2, 3, 4, 5)
        self.motor.set_speed(10000)
        # 0 and 1 are the analog pin  you may need to change them
        self.photo_1 = self.board.get_pin('a:0:i')
        self.photo_2 = self.board.get_pin('a:1:i')
        # adjustment is based on seeing what the rough difference in base
        # values of the two photoresistors is
        adjustment = 100

    def set_angle(self, number):
        print('Angle set to...')
        while 1 == 1:
            input_one = str(self.photo_1.read())
            # initial values for the photoresistors are "None", so that needs to be eliminated so only numbers
            # are read as values, and then the number is divided by 10 so that it is smaller and easier to work with
            if input_one != "None":
                input_one = input_one[2:6]
                input_1 = int(input_one) / 10
            elif input_one == "None":
                input_1 = 0
            input_two = str(self.photo_2.read())
            if input_two != "None":
                input_two = input_two[2:6]
                input_2 = int(input_two) / 10
            elif input_two == "None":
                input_2 = 0

            print("Input 1: " + str(input_1) + "   Input 2: " + str(input_2))
            if abs(input_1 - input_2) > 100:
                if input_1 > input_2:
                    self.motor.step(10)
                    sleep(.01)
                if input_2 > input_1:
                    self.motor.step(-10)
                    sleep(.01)

            else:
                sleep(.01)
