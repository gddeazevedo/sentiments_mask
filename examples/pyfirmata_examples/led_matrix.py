import time
from pyfirmata import Arduino


'''
This code was written by Sam Clane: samclane.github.io/Python-Arduino-PyFirmata/
'''

HIGH = 1
LOW = 0

usb_port = '/dev/ttyACM0'

data_in = 2
load = 4
clock = 3
max_in_use = 1

max_7219_reg_noop = 0x00
max_7219_reg_digit0 = 0x01
max_7219_reg_digit1 = 0x02
max_7219_reg_digit2 = 0x03
max_7219_reg_digit3 = 0x04
max_7219_reg_digit4 = 0x05
max_7219_reg_digit5 = 0x06
max_7219_reg_digit6 = 0x07
max_7219_reg_digit7 = 0x08
max_7219_reg_decode_mode = 0x09
max_7219_reg_intensity = 0x0a
max_7219_reg_scan_limit = 0x0b
max_7219_shutdown = 0x0c
max_7219_reg_display_test = 0x0f


class LedMatrix:
    def __init__(self, board, data_in, load, clock, max_in_use=1):
        self._board = board

        self.pins = dict()
        self.pins['data_in'] = data_in # led matrix pin connected to the Arduino
        self.pins['load'] = load # led matrix pin connected to the Arduino
        self.pins['clock'] = clock # led matrix pi connected to the Arduino
        self.max_in_use = max_in_use

    def _digital_write(self, pin, val):
        self._board.digital[pin].write(val)

    def _put_byte(self, data):
        for i in range(8, 0, -1):
            mask = 0x01 << (i - 1)
            self._digital_write(self.pins['clock'], LOW)
            
            if data & mask:
                self._digital_write(self.pins['data_in'], HIGH)
            else:
                self._digital_write(self.pins['data_in'], LOW)
            
            self._digital_write(self.pins['clock'], HIGH)

    def max_single(self, reg, col):
        self._digital_write(self.pins['load'], LOW)
        self._put_byte(reg)
        self._put_byte(col)
        self._digital_write(self.pins['load'], LOW)
        self._digital_write(self.pins['load'], HIGH)

    def max_all(self, reg, col):
        self._digital_write(self.pins['load'], LOW)
        
        for _ in range(self.max_in_use):
            self._put_byte(reg)
            self._put_byte(col)
        
        self._digital_write(self.pins['load'], LOW)
        self._digital_write(self.pins['load'], HIGH)

    def max_one(self, max_nr, reg, col):
        self._digital_write(self.pins['load'], LOW)
        
        for _ in range(self.max_in_use, max_nr, -1):
            self._put_byte(0)
            self._put_byte(0)

        self._put_byte(reg)
        self._put_byte(col)

        for _ in range(max_nr - 1, 0, -1):
            self._put_byte(0)
            self._put_byte(0)

        self._digital_write(self.pins['load'], LOW)
        self._digital_write(self.pins['load'], HIGH)

    def clear(self):
        for e in range(1, 9):
            self.max_all(e, 0)

    def draw_matrix(self, point_matrix):
        for col, pointlist in enumerate(point_matrix):
            self.max_single(col + 1, int(''.join(str(v) for v in pointlist), 2))

    def setup(self):
        print('Initializing matrix...')
        self._digital_write(13, HIGH)
        self.max_all(max_7219_reg_scan_limit, 0x07)
        self.max_all(max_7219_reg_decode_mode, 0x00)
        self.max_all(max_7219_shutdown, 0x01)
        self.max_all(max_7219_reg_display_test, 0x00)
        self.clear()
        self.max_all(max_7219_reg_intensity, 0x0f & 0x0f)
        print('Done')


def loop(matrix):
    while True:
        matrix.max_single(1, 1)
        matrix.max_single(2, 2)
        matrix.max_single(3, 4)
        matrix.max_single(4, 8)
        matrix.max_single(5, 16)
        matrix.max_single(6, 32)
        matrix.max_single(7, 64)
        matrix.max_single(8, 128)

        time.sleep(.25)

        matrix.max_all(1, 1)
        matrix.max_all(2, 3)
        matrix.max_all(3, 7)
        matrix.max_all(4, 15)
        matrix.max_all(5, 31)
        matrix.max_all(6, 63)
        matrix.max_all(7, 127)
        matrix.max_all(8, 255)

        time.sleep(.25)

        x = [
            [1, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0, 0, 1]
        ]

        matrix.draw_matrix(x)
        time.sleep(.25)
        matrix.clear()
        time.sleep(.25)


if __name__ == '__main__':
    board = Arduino(usb_port)
    matrix = LedMatrix(board, 2, 4, 3)
    matrix.setup()
    loop(matrix)
