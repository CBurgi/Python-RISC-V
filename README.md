# Python RISC-V interpreter
Currently supports
- add
- sub
- addi
- subi
- li
- lw
- sw
- beq
- jal
- jalr
- j

## To run
Create venv, run `python3 processor.py`
- with no arguments will run demo program
### Arguments
- -v: Verbose, prints metrics and registers after every step
- -s: Step, requires input to move to next step
- -r <file.asm>: Read, reads program from any plaintext file
  - demo file `test.asm` included
