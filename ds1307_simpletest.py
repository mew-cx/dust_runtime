# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of reading and writing the time for the DS1307 real-time clock.
# Change the if False to if True below to set the time, otherwise it will just
# print the current date and time every second.
# Notice also comments to adjust for working with hardware vs. software I2C.

import time
import board
import adafruit_ds1307

i2c = board.I2C()
rtc = adafruit_ds1307.DS1307(i2c)

# Lookup table for names of days (nicer printing).
days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

if False:
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2017, 10, 29, 15, 14, 15, 0, -1, -1))
    print("Setting time to:", t)
    rtc.datetime = t
    print()

while True:
    t = rtc.datetime
    # print(t)     # uncomment for debugging
    print("{} {}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        days[int(t.tm_wday)],
        t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
    time.sleep(3)
