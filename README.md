# pico8<->lua
A Python program to extract and insert lua code to a cartridge

# Requeriments
* python 3
* Tkinter

# Usage
`python3 app.py`

The "pico -> lua" option let's you export the lua code of a cartridge to a .lua file generated by the program, that has the same name of your .p8 file.


The "lua -> pico" option requires of a .lua file and .p8 cartridge and replaces any lua code inside your cartridge 
with the one inside your .lua file, if the code size is less than the allowed by PICO-8.
