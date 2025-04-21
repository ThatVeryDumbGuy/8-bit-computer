# **8-bit computer made in Logisim evolution**

## 8bit_computer_V2.circ 
The computer itself
- 1024 of 18 bit instruction memory
- 256 byte data memory
- 14 byte register
- 16 stack layer

## compiler.py
The compiler for the language

Documentation of the language [here](https://github.com/ThatVeryDumbGuy/8-bit-computer/blob/main/language%20documentation.txt)

Spreadsheet of the instruction [here](https://docs.google.com/spreadsheets/d/19sJ7IXaS6HRx7-v0vHk-52AsoSK-bBNAdcGuYu5CgH4/edit?gid=0#gid=0)

MODIFIED VERSIONS OF https://github.com/mattbatwings/BatPU-2/blob/main/assembler.py

## How to use the compiler
1. create a file with no extension
2. put the code into the file and run in cmd "compiler.py [file name]" (make sure that you are in the right directory)
3. the compiled code will be named "Compiled_" + original code name

## Run the program in Logisim
1. find the "PROGRAM_ROM"
2. bottom right there's (click to edit), click it
3. use the "Open..." at the bottom of the hex editor
4. find the compiled code and load it in
5. logisim -> simulate tab at the top left
6. change the auto-tick frequency
7. enable auto-tick
