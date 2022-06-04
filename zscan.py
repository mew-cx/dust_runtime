# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython I2C Device Address Scan"""
import time
import board
import time
import board
import digitalio

i2c = board.I2C()
i2c_power = digitalio.DigitalInOut(board.I2C_POWER)


i2c_power.switch_to_input()
time.sleep(0.01)  # wait for default value to settle
rest_level = i2c_power.value
print("DISABLE rest_level = ", rest_level)


while not i2c.try_lock():
    pass

try:
    for i in range(3):
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in i2c.scan()],
        )
        time.sleep(1)

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()





i2c_power.switch_to_input()
time.sleep(0.01)  # wait for default value to settle
rest_level = i2c_power.value
print("DISABLE rest_level = ", rest_level)
i2c_power.switch_to_output(value=(not rest_level))
print("ENABLE")




while not i2c.try_lock():
    pass

try:
    for i in range(3):
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in i2c.scan()],
        )
        time.sleep(1)

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()


