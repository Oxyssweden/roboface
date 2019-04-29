from time import sleep
from aiy.pins import PIN_D
from gpiozero import LED
from time import sleep

led = LED(PIN_D)

while True:
    led.on()
    sleep(2)
    led.off()
