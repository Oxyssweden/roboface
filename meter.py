from gpiozero import Servo
from time import sleep
from aiy.pins import PIN_D

led = Servo(PIN_D)

    led.min()
    sleep(1)
    led.mid()
    sleep(1)
    led.max()
    sleep(1)
