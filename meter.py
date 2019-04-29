from time import sleep
from aiy.pins import PIN_D
from gpiozero import LED

led = LED(PIN_D)

while True:
    led.on()
    print led.value
    sleep(2)
    led.off()
    print led.value
