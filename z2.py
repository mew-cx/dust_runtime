# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython status NeoPixel red, green, blue example."""
import time
import board
import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

pixel.brightness = 0.3

import time
import board
import digitalio

i2c_power = digitalio.DigitalInOut(board.I2C_POWER)



i2c_power.switch_to_input()
time.sleep(0.01)  # wait for default value to settle
rest_level = i2c_power.value
print("DISABLE rest_level = ", rest_level)


for i in range(2):
    pixel.fill((255, 0, 0))
    time.sleep(0.3)
    pixel.fill((0, 255, 0))
    time.sleep(0.3)
    pixel.fill((0, 0, 255))
    time.sleep(0.3)



i2c_power.switch_to_input()
time.sleep(0.01)  # wait for default value to settle
rest_level = i2c_power.value
print("DISABLE rest_level = ", rest_level)
i2c_power.switch_to_output(value=(not rest_level))
print("ENABLE")



for i in range(2):
    pixel.fill((255, 0, 0))
    time.sleep(0.3)
    pixel.fill((0, 255, 0))
    time.sleep(0.3)
    pixel.fill((0, 0, 255))
    time.sleep(0.3)


