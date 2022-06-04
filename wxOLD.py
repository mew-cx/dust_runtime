# mew 2022-02-13

import time
import board
import microcontroller
import adafruit_ds1307
from adafruit_htu21d import HTU21D
import adafruit_mpl3115a2

i2c = board.I2C()
rtc = adafruit_ds1307.DS1307(i2c)
htu21d = HTU21D(i2c)
mpl3115 = adafruit_mpl3115a2.MPL3115A2(i2c)

daynames = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")

# You can configure the pressure at sealevel to get better altitude estimates.
# This value has to be looked up from your local weather forecast or meteorological
# reports.  It will change day by day and even hour by hour with weather
# changes.  Remember altitude estimation from barometric pressure is not exact!
# Set this to a value in pascals:
mpl3115.sealevel_pressure = 102250

while True:
    print("CPU: %0.3f C" % microcontroller.cpu.temperature)

    t = rtc.datetime
    # print(t)     # for debug
    wday = daynames[int(t.tm_wday)]
    print("DS1307: {} {}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        wday, t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    )

    print("HTU21D: %0.1f C, %0.1f %%RH" % (
        htu21d.temperature, htu21d.relative_humidity))

    print("MPL3115: %0.3f pas, %0.3f m, %0.3f C" % (
        mpl3115.pressure, mpl3115.altitude, mpl3115.temperature))

    print("")

    time.sleep(300)
