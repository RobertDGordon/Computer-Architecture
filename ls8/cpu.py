"""CPU functionality."""

import sys

LDI = 0b10000010 # LDI R0,8

PRN = 0b01000111 # PRN R0

HLT = 0b00000001 # HLT

MUL = 0b10100010 # MUL

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.mdr = 0
        self.mar = 0
        self.halted = False

        self.ir = None

        self.branchtable = {}
        self.branchtable[LDI] = self.ldi # LDI
        self.branchtable[PRN] = self.prn # PRN R0
        self.branchtable[HLT] = self.hlt # HLT
        self.branchtable[MUL] = self.mul # MUL

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        print(f'\nLoading {filename}...\n')
        with open('examples/' + filename + '.ls8') as prog_file:
            address = 0
            for line in prog_file:
                if line[0] == '#' or line[0] == '' or line[0] == '\n':
                    next
                else:
                    # print(line[0:8])
                    instruction = line[0:8]
                    # print(instruction)
                    self.ram[address] = int(instruction, 2)
                    address += 1

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        


    def alu(self, reg_a, reg_b):
        """ALU operations."""
        op = self.ir
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == MUL:
            self.register[reg_a] *= self.register[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    def ldi(self, a, b):
        self.register[a] = b
        self.pc += 3

    def mul(self, a, b):
        self.alu(a, b)
        self.pc += 3

    def prn(self, a, b):
        print('')
        print(self.register[a])
        self.pc +=2

    def hlt(self, a, b):
        print('\nHalting.')
        self.halted = True
        sys.exit(0)

    def run(self):
        print('Running...')
        while not self.halted:
            IR = self.ram[self.pc]
            self.ir = IR
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.branchtable[IR](operand_a, operand_b)
        # print('Halted.')
        # sys.exit(0)
