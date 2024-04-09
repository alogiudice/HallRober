# class ArduinoM, for controlling the motor using an arduino.

import pyfirmata2 as f
from time import sleep

class ArduinoM:
    def __init__(self, stri, motor_pins, relay_pins):
        self.board = f.Arduino(stri)
        self.reader = f.util.Iterator(self.board)
        self.reader.start()
        self.pin_1 = self.board.get_pin('d:%s:o' % (motor_pins[0]))
        self.pin_2 = self.board.get_pin('d:%s:o' % (motor_pins[1]))
        self.pin_3 = self.board.get_pin('d:%s:o' % (motor_pins[2]))
        self.pin_4 = self.board.get_pin('d:%s:o' % (motor_pins[3]))
        self.steps_moved = 0
        self.move_vectors = [[1, 0, 0, 0],
                             [1, 1, 0, 0],
                             [0, 1, 0, 0],
                             [0, 1, 1, 0],
                             [0, 0, 1, 0],
                             [0, 0, 1, 1],
                             [0, 0, 0, 1],
                             [1, 0, 0, 1]
                             ]
        self.move_v_reverse = list(reversed(self.move_vectors))
        # Relay control
        self.relay1 = self.board.get_pin('d:%s:o' % (relay_pins[0]))
        self.relay2 = self.board.get_pin('d:%s:o' % (relay_pins[1]))
        self.relay3 = self.board.get_pin('d:%s:o' % (relay_pins[2]))
        self.relay4 = self.board.get_pin('d:%s:o' % (relay_pins[3]))

    def step(self, vector, delay):
        self.pin_1.write(vector[0])
        self.pin_2.write(vector[1])
        self.pin_3.write(vector[2])
        self.pin_4.write(vector[3])
        sleep(delay)

    def move_new(self, num_step, delay):
        # Se tiene en cuenta que se pudo ahber quedado en un vector intermedio. Por eso,
        # se toma el num de steps recorrido y se ve el resto de dividir por 8 a ver desde donde
        # se arranca a contar.
        i = abs(self.steps_moved % 8)
        j = 0
        if num_step > 0:
            while j < num_step:
                self.step(self.move_vectors[i % 8], delay)
                i += 1
                j += 1
                self.steps_moved += 1
                print("vector[{}]; total steps: {}".format(i % 8, self.steps_moved))
        elif num_step < 0:
            while j < abs(num_step):
                self.step(self.move_v_reverse[i % 8], delay)
                i += 1
                j += 1
                self.steps_moved -= 1
                print("vector[{}]; total steps: {}".format(i % 8, self.steps_moved))

    def turnoff_motor(self):
        # Veo si puedo evitar que el motor siga llevandose corriente cuando no lo necesito
        # (y que hace que el relay quede inutilizable)
        self.step([0, 0, 0, 0], 1)


    def steps_to_angle(self, steps):
        # steps to angle conversion
        # El motor 28byj-48 tiene 4096 pasos por vuelta.
        angle = steps * 360 / 4095
        return round(angle)

    def angle_to_steps(self, angle):
        step = angle * (4095) / 360
        return round(step)

    def change_relay_config(self, config):
        # 1 is forward and -1 is reverse.
        if config == 1:
            self.relay1.write(0)
            self.relay2.write(1)
            self.relay3.write(1)
            self.relay4.write(0)
            print('Relays 1 and 4 on (forward config)')
        elif config == -1:
            self.relay1.write(1)
            self.relay2.write(0)
            self.relay3.write(0)
            self.relay4.write(1)
            print('Relays 2 and 3 on (inverse config)')
        else:
            print('No change in relay configuration')
