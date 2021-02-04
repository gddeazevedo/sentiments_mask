import pyfirmata
import time


usb_port = '/dev/ttyACM0'
board = pyfirmata.Arduino(usb_port)


leds = [
    board.get_pin('d:12:o'),
    board.get_pin('d:7:o'),
    board.get_pin('d:4:o'),
    board.get_pin('d:3:o')
]


while True:
    for led in leds:
        led.write(1)

    time.sleep(1)

    for led in leds:
        led.write(0)

    time.sleep(1)