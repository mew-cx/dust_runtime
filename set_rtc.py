# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_ds1307

i2c = board.I2C()
rtc = adafruit_ds1307.DS1307(i2c)

t = time.struct_time((
    2022,  # year
    4,     # month
    5,     # date
    1,    # hour
    2,    # minute
    3,    # second
    2,     # weekday (0=Sun..6=Sat)
    -1,    # yearday, not used
    -1     # isdst, not used
))
rtc.datetime = t
print("Setting time to:", t)

