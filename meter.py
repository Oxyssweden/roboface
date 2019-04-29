from gpiozero import PWMLED
from time import sleep
from aiy.pins import PIN_D

led = PWMLED(PIN_D)

while True:
    led.value = 0.1
    sleep(1)
    led.off()
