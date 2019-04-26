#!/usr/bin/env python3
"""
This is an example of how the pytradfri-library can be used.

To run the script, do the following:
$ pip3 install pytradfri
$ Download this file (example_sync.py)
$ python3 example_sync.py <IP>

Where <IP> is the address to your IKEA gateway. The first time
running you will be asked to input the 'Security Code' found on
the back of your IKEA gateway.
"""

"""Trigger PiCamera when face is detected."""


# Hack to allow relative import above top level package
import sys
import os
folder = os.path.dirname(os.path.abspath(__file__))  # noqa
sys.path.insert(0, os.path.normpath("%s/.." % folder))  # noqa

from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json

import uuid
import argparse
import threading
import time

from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection

from picamera import PiCamera

CONFIG_FILE = 'tradfri_standalone_psk.conf'


parser = argparse.ArgumentParser()
parser.add_argument('host', metavar='IP', type=str,
                    help='IP Address of your Tradfri gateway')
parser.add_argument('-K', '--key', dest='key', required=False,
                    help='Security code found on your Tradfri gateway')
args = parser.parse_args()


if args.host not in load_json(CONFIG_FILE) and args.key is None:
    print("Please provide the 'Security Code' on the back of your "
          "Tradfri gateway:", end=" ")
    key = input().strip()
    if len(key) != 16:
        raise PytradfriError("Invalid 'Security Code' provided.")
    else:
        args.key = key


def run():
    # Assign configuration variables.
    # The configuration check takes care they are present.
    conf = load_json(CONFIG_FILE)

    try:
        identity = conf[args.host].get('identity')
        psk = conf[args.host].get('key')
        api_factory = APIFactory(host=args.host, psk_id=identity, psk=psk)
    except KeyError:
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host=args.host, psk_id=identity)

        try:
            psk = api_factory.generate_psk(args.key)
            print('Generated PSK: ', psk)

            conf[args.host] = {'identity': identity,
                               'key': psk}
            save_json(CONFIG_FILE, conf)
        except AttributeError:
            raise PytradfriError("Please provide the 'Security Code' on the "
                                 "back of your Tradfri gateway using the "
                                 "-K flag.")

    api = api_factory.request

    gateway = Gateway()

    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    lights = [dev for dev in devices if dev.has_light_control]

    # Print all lights
    print(lights)

    # Lights can be accessed by its index, so lights[1] is the second light
    if lights:
        light = lights[0]
    else:
        print("No lights found!")
        light = None

    if light:
        light_command = light.light_control.set_dimmer(254)
        dark_command = light.light_control.set_dimmer(0)
        api(dark_command)

        with PiCamera() as camera:
            # Configure camera
            camera.resolution = (1640, 922)  # Full Frame, 16:9 (Camera v2)
            camera.start_preview()

            # Do inference on VisionBonnet
            with CameraInference(face_detection.model()) as inference:
                for result in inference.run():
                    if len(face_detection.get_faces(result)) >= 1:
                        print('I see you')
                        api(light_command)
                        time.sleep(120)
                        api(dark_command)

def main():
    try:
        run()
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.exception('Exception while running script.')
        if args.blink_on_error:
            with Leds() as leds:
                leds.pattern = Pattern.blink(100)  # 10 Hz
                leds.update(Leds.rgb_pattern(Color.RED))
                time.sleep(1.0)

    return 0

if __name__ == '__main__':
    sys.exit(main())
