import sys
import os

# opcodes and their argument count
opcodes = {
    "add": 3,
    "sub": 3,
    "addi": 3,
    "subi": 3,
    "li": 2,
    "lw": 3,
    "sw": 3,
    "beq": 3,
    "jal": 2,
    "jalr": 3,
    "j": 1
}


class Processor:
    def __init__(self, v, s, file):
        self.v = v
        self.s = s

        self.file = []
        if file:
            with open(file, 'r') as f:
                for line in f:
                    self.file.append(line.strip())
        else:
            self.file = file

        self.pc = 0
        self.reg = {}
        for i in range(32):
            self.reg[f"x{i}"] = 0
        self.mem = [0] * 32  # data memory

        self.prog_mem = []
        self.sections = {}  # map pc count to section

    # ADD, SUB, LI, LW, SW, BEQ, JAL

    def add(self, rd, rs1, rs2):
        if rd != 0:
            self.reg[rd] = self.reg[rs1] + self.reg[rs2]
        return True

    def sub(self, rd, rs1, rs2):
        if rd != 0:
            self.reg[rd] = self.reg[rs1] - self.reg[rs2]
        return True

    def addi(self, rd, rs1, imm):
        if rd != 0:
            self.reg[rd] = self.reg[rs1] + int(imm)
        return True

    def subi(self, rd, rs1, imm):
        if rd != 0:
            self.reg[rd] = self.reg[rs1] - int(imm)
        return True

    def li(self, rd, imm):
        self.addi(rd, 'x0', imm)
        return True

    def lw(self, rd, imm, rs1):
        if rd != 0:
            self.reg[rd] = self.mem[self.reg[rs1] + int(imm)]
        return True

    def sw(self, src, imm, rs1):
        self.mem[self.reg[rs1] + int(imm)] = self.reg[src]
        return True

    def beq(self, rs1, rs2, label):
        if label in self.sections:
            if self.reg[rs1] == self.reg[rs2]:
                self.pc = self.sections[label]
                return False
        return True

    def jal(self, rd, imm):
        if rd != 0:
            self.reg[rd] = self.pc + 1
        if isinstance(imm, str):
            if imm in self.sections:
                self.pc = self.sections[imm]
        else:
            self.pc = int(imm)
        return False

    def j(self, imm):
        self.jal('x0', imm)
        return False

    def jalr(self, rd, rs1, imm):
        if rd != 0:
            self.reg[rd] = self.pc + 1
        self.pc = self.reg[rs1] + int(imm)
        return False

    def print_metrics(self, title, i, c):
        os.system('clear')
        print(title)
        print("Metrics:")
        print(f"{i} instructions, {c} cycles")
        print("")
        print("Registers:")
        print(f"PC: {self.pc}")
        items = list(self.reg.items())
        for i in range(0, 32, 8):
            row = items[i:i + 8]
            # Join the elements of the row with a tab
            print("\t".join([f"{k}: {v}" for k, v in row]))

        if(any(self.mem)):
            str_mem = [str(item) for item in self.mem]
            print("")
            print("Memory:")
            for i in range(4):
                print('\t'.join(str_mem[8*i:8*i+8]))

    def run(self, program):
        try:
            self.pc = 0
            for r in self.reg:
                self.reg[r] = 0
            self.mem = [0] * 32  # data memory

            self.prog_mem = []
            self.sections = {}  # map pc count to section

            # load program into prog mem
            if self.file:
                program = self.file
            index = 0
            print(program)
            for line in program:
                if line.endswith(":"):
                    section = line[:-1]
                    self.sections[section] = index
                else:
                    command = line.split(" ")
                    opcode = command[0].lower()
                    args = command[1:]
                    if opcode in opcodes and opcodes[opcode] == len(args):
                        self.prog_mem.append(
                            {"opcode": opcode, "args": args}
                        )
                        index += 1

            i_count = 0
            c_count = 0

            # run program
            while True:
                c_count += 1

                i_count += 1
                line = self.prog_mem[self.pc]
                func = getattr(self, line["opcode"])
                inc = func(*line["args"])
                if inc:
                    self.pc += 1
                if self.s:
                    input("Enter to step")
                if self.v:
                    self.print_metrics(
                        f"{line['opcode']} {' '.join(line['args'])}",
                        i_count,
                        c_count
                    )
                if self.pc >= len(self.prog_mem):
                    break
        except:
            print("Program failed")
        finally:
            # print results
            self.print_metrics(
                "-------Program Finished-------",
                i_count,
                c_count
            )


program1 = [
    "li x2 1",
    "li x3 10",
    "add x2 x3 x2",
    "add x2 x3 x2",
    "add x2 x3 x2",
    "add x2 x3 x2",
    "add x2 x3 x2"

]

program2 = [
    "li x2 123353",
    "li x3 45551",

    "sub x2 x3 x2",
    "sub x2 x3 x2",
    "sub x2 x3 x2",
    "sub x2 x3 x2",
    "sub x2 x3 x2"

]

program3 = [
    "li x2 577",
    "li x3 555",
    "li x5 443",
    "SUB x2 x3 x2",
    "SUB x2 x3 x2",
    "ADD x2 x5 x3",
    "ADD x2 x2 x2",
    "SUB x2 x3 x2",
    "SUB x2 x3 x2",
    "SUB x2 x3 x2",
    "ADD x5 x3 x2",
    "ADD x3 x2 x3"
]

program4 = [
    "start:",
    "LI x3 1",
    "LI x5 10",
    "count_loop:",
    "BEQ x3 x5 done",
    "JAL x1 increment",
    "J count_loop",
    "increment:",
    "ADDi x3 x3 1",
    "Jalr x0 x1 0",
    "done:",
    "J done"
]

args = [
    '-v',
    '-s',
    '-r'
]
if __name__ == "__main__":
    v = '-v' in sys.argv
    s = '-s' in sys.argv
    file = False
    if '-r' in sys.argv:
        try:
            file = sys.argv[sys.argv.index('-r') + 1]
            if file in args:
                raise IndexError
            open(file, 'r')
        except:
            print("Add valid file path as argument after -r")
            exit(1)
    p = Processor(v, s, file)
    p.run(program4)
