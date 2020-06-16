"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter
        # register is where you store what you retrieved from ram(memory)
        self.reg = [0] * 8 # variable R0-R7
        # ram is running memory
        self.ram = [0] * 256 # ram is memory
        self.branch_table = {}
        self.branch_table[LDI] = self.handle_ldi
        self.branch_table[PRN] = self.handle_prn
        self.branch_table[MUL] = self.handle_mul
        

    def ram_read(self, address):
        # Memory_Address_Register = MAR
        # MAR

        # takes address and returns the value at the address
        return self.ram[address]
    
    def ram_write(self, value, address):
        # Memory_Data_Register = MDR
        
        # takes an address and a value to write to it
        self.ram[address] = value


    def load(self):
        """Load a program into memory."""

        # sets up a way to read the program being passed in by a user
        filename = sys.argv[1]
        # print("filename", filename)
        address = 0
        with open(filename) as f:
            for line in f:
                line = line.split("#")

                try:
                    value = int(line[0], 2)

                except ValueError:
                    continue

                # self.ram[address] = value
                self.ram_write(value, address)
                address += 1
    
    def handle_ldi(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc += 3
    
    def handle_prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def handle_mul(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)
        # prod = self.reg[reg_1] * self.reg[reg_2]
        # self.reg[reg_1] = prod

        # use the alu to run the multiplication on the register values
        self.alu("MUL", reg_1, reg_2)
        self.pc += 3



        # defines where to write to ram
        # only used in the load method
        # address = 0 

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8 (save to reg)
        #     0b00000000, # index 1
        #     0b00001000, # value at 1
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # brings instructions and all from program and writes to ram (memory)
        # so it can then be accessed by the CPU
        # for instruction in program:
        #     self.ram_write(instruction, address)
        #     address += 1 
            # just used to increment through the ram addresses


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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


    def run(self):
        """Run the CPU."""
        # instrution register
        ir = LDI
        self.branch_table[ir]()
        ir = LDI
        self.branch_table[ir]()
        ir = MUL
        self.branch_table[ir]()
        ir = PRN
        self.branch_table[ir]()


        # running = True

        # while running:
        #     # instruction register
        #     ir = self.ram[self.pc]
            
        #     if ir == self.ram[0]:
        #         # arranges data from bucket
        #         # where will you put it in your pocket?
        #         # this is putting it in your pocket
        #         # "where" is the reg_num: it is  the indice of the reg array
        #         reg_num = self.ram[self.pc + 1]
        #         value = self.ram[self.pc + 2]
        #         self.register[reg_num] = value
        #         self.pc += 3
            
        #     # print instruction
        #     elif ir == self.ram[3]: 
        #         reg_num = self.ram[self.pc + 1]
        #         print(self.register[reg_num])
        #         self.pc += 2

        #     elif ir == self.ram[6]:
        #         reg_num = self.ram[self.pc]
            
        #     elif ir == self.ram[5]:
        #         running = False
        #         self.pc += 1
            
            
        #     else:
        #         print(f'Unknown instruction{ir} at address {self.pc}')
        #         sys.exit(1)




