import pyfirmata
import time


usb_port = '/dev/ttyACM0'
board = pyfirmata.Arduino(usb_port)

it = pyfirmata.util.Iterator(board)
it.start()


button = board.get_pin('d:4:i') # pin type : pin number : pin mode
led = board.get_pin('d:10:o')

# board.digital[4].mode = pyfirmata.INPUT
# board.digital[10].mode = pyfirmata.OUTPUT
#
##

while True:
    is_pressed = button.read()

    if is_pressed:
        led.write(1)
    else:
        led.write(0)

    time.sleep(0.1)
