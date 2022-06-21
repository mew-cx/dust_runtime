import microcontroller
mode = microcontroller.RunMode.UF2
#mode = microcontroller.RunMode.BOOTLOADER
microcontroller.on_next_reset(mode)
microcontroller.reset()
