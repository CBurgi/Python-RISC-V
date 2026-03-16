pc = 0

reg = [0] * 32 #registers (no fp)
x0 = zero = 0
x1 = ra = 1
x2 = sp = 2
x3 = gp = 3
x4 = tp = 4
x5 = t0 = 5
x6 = t1 = 6
x7 = t2 = 7
x8 = s0 = fp = 8
x9 = s1 = 9
x10 = a0 = 10
x11 = a1 = 11
x12 = a2 = 12
x13 = a3 = 13
x14 = a4 = 14
x15 = a5 = 15
x16 = a6 = 16
x17 = a7 = 17
x18 = s2 = 18
x19 = s3 = 19
x20 = s4 = 20
x21 = s5 = 21
x22 = s6 = 22
x23 = s7 = 23
x24 = s8 = 24
x25 = s9 = 25
x26 = s10 = 26
x27 = s11 = 27
x28 = t3 = 28
x29 = t4 = 29
x30 = t5 = 30
x31 = t6 = 31

mem = [0] * 32 #data memory

prog_mem = []
sections = [] #map pc count to section

#ADD, SUB, LI, LW, SW, BEQ, JAL
def add(rd, rs1, rs2):
    if rd == 0:
        return
    reg[rd] = reg[rs1] + reg[rs2]

def sub(rd, rs1, rs2):
    if rd == 0:
        return
    reg[rd] = reg[rs1] - reg[rs2]

def li(rd, imm):
    if rd == 0:
        return
    reg[rd] = imm

def lw(rd, imm, rs1):
    if rd == 0:
        return
    reg[rd] = mem[reg[rs1] + imm]

def sw(src, imm, rs1):
    mem[reg[rs1] + imm] = reg[src]

def beq(rs1, rs2, label):
    global pc
    if label in sections:
        if reg[rs1] == reg[rs2]:
            pc = sections[label]

def j(label):
    global pc
    if label in sections:
        pc = sections[label]

def jal(rd, imm):
    global pc
    reg[rd] = pc + 1
    if isinstance(imm, str):
        if imm in sections:
            pc = sections[imm]
    else:
        pc += imm

class Processor:
    pc = 0
    i_count = 0
    c_count = 0
    
  
  
  
program1 = [
    "li 2 1" 
    "li 3 10"
    "add 2 3 2"
    "add 2 3 2"
    "add 2 3 2"
    "add 2 3 2"
    "add 2 3 2"
    
]

program2 = [
    "li 2 123353"
    "li 3 45551"
    
    "sub 2 3 2"
    "sub 2 3 2"
    "sub 2 3 2"
    "sub 2 3 2"
    "sub 2 3 2"

]

program3 = [
    "li 2 577"
    "li 3 555"
    "li 5 443"
    "SUB 2 3 2"
    "SUB 2 3 2"
    "ADD 2 5 3"
    "ADD 2 2 2"
    "SUB 2 3 2"
    "SUB 2 3 2"
    "SUB 2 3 2"
    "ADD 5 3 2"
    "ADD 3 2 3"
]

program4 = [
    "start:"
        "LI 3 1"
        "LI 5 10"
    "count_loop:"
        "BEQ 3, 5, done"
        "JAL increment"
        "J count_loop"
    "increment:"
        "ADD 3 3 1"
    "done:"
        "J done"
] 
