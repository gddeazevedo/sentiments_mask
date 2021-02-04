import pyfirmata
import time


usb_port = '/dev/ttyACM0'
board = pyfirmata.Arduino(usb_port)

it = pyfirmata.util.Iterator(board)
it.start()


analog_input = board.get_pin('a:0:i')
led = board.get_pin('d:12:o')


while True:
    analog_value = analog_input.read()

    if analog_value is not None:
        delay = analog_value + 0.01
        led.write(1)
        time.sleep(delay)
        led.write(0)
        time.sleep(delay)
    else:
        time.sleep(0.1)
