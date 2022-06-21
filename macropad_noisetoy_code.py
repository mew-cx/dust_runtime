

# macropad_noisetoy.py -- what in the heck
# This started as a demonstration of a simple 'Toner' class to play PWM tones
# in a non-blocking way. I've since messed that all up
# @todbot 14 Aug 2021 
import time,random
import board, digitalio, pwmio
import rainbowio
import displayio, terminalio
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_macropad import MacroPad
from supervisor import ticks_ms   # ticks_ms() yay!

macropad = MacroPad(rotation=90)
encoder = macropad._encoder # we want raw encoder
leds = macropad.pixels
macropad._speaker_enable.value = True  # we'll control on/off via duty_cycle

# make a da beeps    
class Toner:
    def __init__(self, pin, frequency, duration, duty_cycle=32768): 
        self._duration = int(duration*1000) # we're a millisecs house 
        self._start_time = ticks_ms()
        self._tone = pwmio.PWMOut(pin, frequency=frequency, variable_frequency=True)
        self._duty_cycle = duty_cycle
        self._tone.duty_cycle = duty_cycle
        self.isplaying = True

    def update(self):
        if ticks_ms() - self._start_time > self._duration:
            self.isplaying = False
            self._tone.duty_cycle = 0 # stop tone

    def tone(self, frequency, duration, duty_cycle=None):
        self._duration = int(duration*1000)
        self._start_time = ticks_ms()
        if duty_cycle is not None:
            self._tone.duty_cycle = duty_cycle
        self._tone.frequency = frequency
        self.isplaying = True
    
# how to fake an enum in Python
class EditMode:
    NONE = 0
    NOTE = 1
    DUTY_CYCLE = 2
    DURATION = 3
    PITCH = 4

screen = displayio.Group()  # a main group that holds everything
macropad.display.show(screen)  # add main group to display

ltitle = label.Label(terminalio.FONT,text="noisetoy", x=5, y=5)
ldclfo = label.Label(terminalio.FONT,text="dclfo:000", x=5, y=30)
lplfo  = label.Label(terminalio.FONT,text="plfo:000", x=5, y=50)
loct   = label.Label(terminalio.FONT,text="oct:0", x=5, y=70)
ldur   = label.Label(terminalio.FONT,text="dur:000", x=5, y=90)
lmode =  label.Label(terminalio.FONT,text="-", x=56, y=120)
screen.append(ltitle)
screen.append(ldclfo)
screen.append(lplfo)
screen.append(loct)
screen.append(ldur)
screen.append(lmode)

# calling this function really messes up the timing
def update_display(mode=EditMode.NONE):
    if mode == EditMode.NONE:
        if seq_playing:
            leds[11] = 0x00ff00 
            lmode.text = ">"
        else:
            leds[11] = 0xff0000
            lmode.text = "="

    if mode == EditMode.DUTY_CYCLE or mode == EditMode.NONE:
        ldclfo.text = "%s:%03x" % ("DCLFO" if duty_cycle_enable else "dclfo",
                                   abs(duty_cycle_inc//8))
    if mode == EditMode.PITCH or mode == EditMode.NONE:
        lplfo.text = "%s:%f" % ("PLFO" if pitch_lfo_enable else "plfo", 0.1) # FIXME
    if mode == EditMode.NOTE or mode == EditMode.NONE:
        loct.text = "oct:%d" % (note_octave)
    if mode == EditMode.DURATION or mode == EditMode.NONE:
        ldur.text = "dur:%2.2f" % (note_duration)

notes0  = [130, 147, 165, 174, 196, 220, 247]
notes0a = notes0[::-1]  # reversed
#        C4    D4   E4   F4    G4   A4  B4
notes1 = [262, 294, 330, 349, 392, 440, 494]
#notes2 = [n*2 for n in notes1]  # this is such a hack
#notes3 = [n//2 for n in notes1]
notes = notes0
note = notes[0] # note currently being played
note_duration = 0.1
note_index = 0
note_octave=0

duty_cycle_enable = False
duty_cycle_default = 32768 # 1000 gives lower volume
duty_cycle = duty_cycle_default 
duty_cycle_inc = 170

pitch_lfo_enable = False
pitch_lfo = 1.0
pitch_lfo_inc = 0.1  # FIXME: percentage of current note
#pitch_lfo_max = 0.3

seq_playing = True
audio_playing = True
encoder_pos = encoder.position
encoder_pos_save = encoder_pos

note_durs = 10
note_dur_delta = 0.01

if not audio_playing:  # FIXME HACK
    duty_cycle = 0

toner = Toner(board.SPEAKER, frequency=note,
              duration=note_duration, duty_cycle=duty_cycle)

mode = EditMode.NONE

print_time = ticks_ms()

update_display()
import gc
while True:
    toner.update()
    
    # user input: encoder switch
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        macropad._speaker_enable.value = not macropad._speaker_enable.value 
        
    # user input: keys
    key = macropad.keys.events.get()
    if key:
        print("KEY: ",key.key_number, key.pressed, key.released)
        if key.pressed:
            if key.key_number == 0:
                notes = notes0
            elif key.key_number == 1:
                notes = notes0a
            elif key.key_number == 8:  # DUTY_CYCLE LFO edit on
                mode = EditMode.DUTY_CYCLE
                encoder_pos_save = encoder_pos
            elif key.key_number == 9: # PITCH LFO
                mode = EditMode.PITCH
                encoder_pos_save = encoder_pos
            elif key.key_number == 10:  # NOTE_DURATION
                mode = EditMode.DURATION
                encoder_pos_save = encoder_pos
            elif key.key_number == 11: # PLAYING
                mode = EditMode.NOTE
                encoder_pos_save = encoder_pos
                #seq_playing = not seq_playing
        if key.released:
            mode = EditMode.NONE
            if key.key_number == 8: # DUTY_CYCLE edit off
                if encoder_pos == encoder_pos_save:
                    duty_cycle_enable = not duty_cycle_enable
            elif key.key_number == 9: # PITCH LFO
                if encoder_pos == encoder_pos_save:
                    pitch_lfo_enable = not pitch_lfo_enable
            elif key.key_number == 10: # NOTE_DURATION edit off
                pass
            elif key.key_number == 11: #
                if encoder_pos == encoder_pos_save:
                    seq_playing = not seq_playing
        update_display(mode)

    # user input: encoder turn handling
    delta = encoder_pos - encoder.position
    if delta != 0:
        encoder_pos = encoder.position
        if mode == EditMode.DUTY_CYCLE: # change duty cycle
            duty_cycle_inc = duty_cycle_inc + (delta * 200)
            print("  DUTY", duty_cycle_enable, duty_cycle_inc)
        elif mode == EditMode.DURATION: # change note duration
            note_durs += delta
            note_duration =  min(max(note_durs * note_dur_delta,0),10)
        elif mode == EditMode.PITCH:
            pitch_lfo_inc = pitch_lfo_inc + (delta/100)
            #pitch_lfo_inc = pitch_lfo_inc + (delta/100)
            print("   PITCH", pitch_lfo_inc, pitch_lfo)
        elif mode == EditMode.NOTE:
            print("    NOTE", note_octave)
            note_octave  = min(max(note_octave + delta, 0), 4)
        else:
            pass
        if mode != EditMode.NONE:
            update_display(mode)
        
    if audio_playing:
        if duty_cycle_enable:
            duty_cycle = duty_cycle + duty_cycle_inc
            duty_cycle = duty_cycle % 65535
            toner._tone.duty_cycle = duty_cycle
        if pitch_lfo_enable:
            # this is wrong
            pitch_lfo = pitch_lfo + pitch_lfo_inc # orbit around 1.0
            if pitch_lfo > 1.3 or pitch_lfo < 0.7: # up-down
                pitch_lfo_inc = -pitch_lfo_inc 
            toner._tone.frequency = int(note + pitch_lfo) # FIXME
            
    # note done, go to next note
    if not toner.isplaying:
        if ticks_ms() - print_time > 1000:
            print_time = ticks_ms()
            print(ticks_ms(),"mode:%d seq:%d aud:%d dc:%d p:%d (%2.2f) dur:%f note:%d" %
                  (mode, seq_playing, audio_playing, duty_cycle_enable, pitch_lfo_enable,
                   pitch_lfo_inc, note_duration, note))

        if seq_playing:
            note_index = (note_index+1) % len(notes)
            note = notes[note_index]
            note = note * (note_octave+1)
            toner.tone(note, note_duration, duty_cycle=duty_cycle)
            n = note_index % len(leds)
            leds[ n ] = rainbowio.colorwheel( ticks_ms() %255)
        


# Misc thoughts:
#
# - Uses "ticks_ms()" so requires CP7 alpha6 or better
#
# - Parameters we can control:
#   - note scale ; need more scales!
#   - note scale length (plus octaves)
#   - beats per minute, i.e. note rate
#   - note duration? (vs bpm, stacato vs legato, possible?)
#   - duty_cycle LFO on/off
#   - duty_cycle LFO rate
#   - pitch LFO on/off
#   - pitch LFO rate
#
# - Are keys "mode switches" or "sequence note on/off"? (I think mode switches)
#   - this is not a sequencer, it's a noisy boi
# - How to do display updates without destroying timing
#   - selective update: determine what changes, only update that (CircuitPythonReact!)
#   - update always, absorb the delay and suck it up
#   - update only on note change: limits high-rate chaos mode
#
