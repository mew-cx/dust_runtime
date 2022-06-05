# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_ds1307
import rtc

t = time.struct_time((
    2021,  # year
    2,     # month
    3,     # date
    4,     # hour
    5,     # minute
    6,     # second
    2,     # weekday (0=Sun..6=Sat)
    -1,    # yearday, not used
    -1     # isdst, not used
))
print("t:\t\t", t)

print("time.localtime:\t", time.localtime())

i2c = board.I2C()
ds = adafruit_ds1307.DS1307(i2c)
#ds.datetime = t
print("ds.datetime:\t", ds.datetime)

r1 = rtc.RTC()
print("r1.datetime1:\t", r1.datetime)
rtc.set_time_source(ds)
print("r1.datetime2:\t", r1.datetime)
