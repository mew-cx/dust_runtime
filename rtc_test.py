# rtc_test.py -- mew@mew.cx 2002-06-04
# SPDX-FileCopyrightText: 2022 Mike Weiblen

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_ds1307
import rtc

print("time.localtime:\t", time.localtime())

i2c = board.I2C()
ds = adafruit_ds1307.DS1307(i2c)
print("ds.datetime:\t", ds.datetime)

r1 = rtc.RTC()
print("r1.datetime1:\t", r1.datetime)

# !!!!! Try to install the ds1307 as the time source.
rtc.set_time_source(ds)

# !!!!! shouldn't this now print the DS1307 time??
r2 = rtc.RTC()
print("r2.datetime2:\t", r2.datetime)
