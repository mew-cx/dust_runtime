# uname/code.py

print("\nsysinfo ==================")

import board
print("board.board_id :", board.board_id)
print("dir(board) :", dir(board))

import os
#print("\ndir(os) :", dir(os))
print("os.uname() :", os.uname())

import supervisor
#print("\ndir(supervisor) :", dir(supervisor))

import microcontroller
print("\ndir(microcontroller) :", dir(microcontroller))
print("dir(microcontroller.pin) :", dir(microcontroller.pin))

import sys
print("\ndir(sys) :", dir(sys))
print("sys.version :", sys.version)
print("sys.platform :", sys.platform)
print("sys.implementation :", sys.implementation)
print("sys.path :", sys.path)
#print("sys.modules :", sys.modules)

import micropython
#print("\ndir(micropython) :", dir(micropython))

print("\nhelp('modules') {")
help('modules')
print("}")

import pin_map
print("==========================")
