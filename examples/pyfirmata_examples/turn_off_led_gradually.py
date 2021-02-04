import time
import pyfirmata


usb_port = 'COM3'
board = pyfirmata.Arduino(usb_port)

it = pyfirmata.util.Iterator(board)
it.start()


led = board.get_pin('d:9:p')


while True:
    led.write(150)
