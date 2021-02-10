HIGH = 1
LOW = 0

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

    def clear(self):
        for e in range(1, 9):
            self.max_all(e, 0)

    def draw_matrix(self, point_matrix):
        for col, pointlist in enumerate(point_matrix):
            self.max_single(col + 1, int(''.join(str(v) for v in pointlist), 2))

    def setup(self):
        self._digital_write(13, HIGH)
        self.max_all(max_7219_reg_scan_limit, 0x07)
        self.max_all(max_7219_reg_decode_mode, 0x00)
        self.max_all(max_7219_shutdown, 0x01)
        self.max_all(max_7219_reg_display_test, 0x00)
        self.clear()
        self.max_all(max_7219_reg_intensity, 0x0f & 0x0f)
