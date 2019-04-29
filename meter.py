from gpiozero import PWMLED
from time import sleep
from aiy.pins import PIN_D

led = PWMLED(PIN_D)

led.value = 0.5
sleep(2)
led.off()
