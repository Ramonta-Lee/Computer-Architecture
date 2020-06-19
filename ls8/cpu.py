"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b1000101
POP = 0b1000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter
        self.flag = 0b00000000
        # register is where you store what you retrieved from ram(memory)
        self.reg = [0] * 8 # variable R0-R7
        # ram is running memory
        self.ram = [0] * 256 # ram is memory
        self.sp = 7
        self.reg[self.sp] = 0xF4 # where in
        self.branch_table = {
            LDI:self.handle_ldi,
            PRN:self.handle_prn,
            MUL:self.handle_mul,
            HLT:self.handle_hlt,
            PUSH: self.handle_push,
            POP:self.handle_pop,
            CALL: self.handle_call,
            RET:self.handle_ret,
            ADD:self.handle_add,
            CMP: self.handle_cmp,
            JEQ: self.handle_jeq,
            JNE: self.handle_jne,
            JMP: self.handle_jmp
        }


    def ram_read(self, address):
        # Memory_Address_Register = MAR
        # MAR

        # takes address and returns the value at the address
        # print(self.ram[address])
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
                # print(line)
                line = line.split("#")
                # print(line)

                try:
                    value = int(line[0], 2)
                    # print("value", value)

                except ValueError:
                    continue

                # self.ram[address] = value
                # address += 1
                self.ram_write(value, address)
                address += 1
    
    def handle_ldi(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc += 3
    
    def handle_prn(self):
        print("hello", self.reg[self.ram_read(self.pc + 1)])
        # self.trace()
        self.pc += 2

    def handle_mul(self):
        # goes to address R0 & R1
        # reads and returns the values
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        # use the alu to run the multiplication on the register values
        self.alu("MUL", reg_1, reg_2)
        self.pc += 3

    def handle_add(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        self.alu("ADD", reg_1, reg_2)
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
    
    def handle_push(self):
        # decrement SP
        self.reg[self.sp] -= 1

        # Get the value we want to store from the register
        # address
        reg_1 = self.ram_read(self.pc + 1)
        


        # this is the value that we want to push
        value = self.reg[reg_1]

        # Figure out where to store
        top_of_stack_addr = self.reg[self.sp]

        # Store it!
        # self.ram[top_of_stack_addr] = value
        # print("val", value)

        self.ram_write(value, top_of_stack_addr)
        # print("ram", self.ram)

        self.pc += 2
    
    def handle_pop(self):
        # check to see if stack is empty
        if self.reg[self.sp] == 0xF4:
            return print("Empty Stack")

        # get the location of what we are trying to remove
        reg_indx = self.ram_read(self.pc + 1)
        # print("val", value)
        self.reg[reg_indx] = self.ram[self.reg[self.sp]] # sets register at reg index equal to top of the stack (by way of pointer; SP)
        

        # increment the start pointer
        self.reg[self.sp] += 1

        # increment the program counter
        self.pc += 2
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        #elif op == "SUB": etc
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        
        elif op == "CMP":

            if self.reg[reg_a] > self.reg[reg_b]:
                #100
                self.flag = 0b00000100
            
            elif self.reg[reg_a] < self.reg[reg_b]:
                #010
                self.flag = 0b00000010
            
            else:
                  self.flag = 0b00000001
            
            

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
    
    def handle_call(self):
        # store the return address
        return_addr = self.pc + 2

        # decrement the start pointer
        self.reg[self.sp] -= 1
        # pushing the return address on to the stack
        self.ram[self.reg[self.sp]] = return_addr

        # Get the address to call
        reg_num = self.ram[self.pc + 1]
        # store the sub addr
        subroutine_addr = self.reg[reg_num]

        # Call it!
        # Moves the pointer to the sub
        self.pc = subroutine_addr



    def handle_ret(self):
        # Get the location of what you want to remove
        # return_addr = self.ram[self.pc + 2]

        # # In the register, at the return address. Set it equal to memory at the register address where the start pointer is pointing
        # self.reg[return_addr] = self.ram[self.reg[self.sp]]

        # # increment the start pointer
        # self.reg[self.sp] += 1

        
        # self.pc = return_addr


        reg_indx = self.ram[self.pc + 1]
        # print("val", value)
        self.reg[reg_indx] = self.ram[self.reg[self.sp]] # sets register at reg index equal to top of the stack (by way of pointer; SP)
        

        # increment the start pointer
        self.reg[self.sp] += 1

        # store popped element from stack in the pc
        # return the counter to where we were before the call (after call instruction
        #)
        self.pc = self.reg[reg_indx]


    
    def handle_hlt(self):
        self.pc += 1
        self.running = False
        return self.running


    def run(self):
        """Run the CPU."""
        # instrution register
        self.running = True
        while self.running:
            ir = self.ram[self.pc]
            if ir in self.branch_table:
                self.branch_table[ir]()
            
            else:
                print(f'Unknown instruction: {ir}, at address PC: {self.pc}')
                sys.exit(1)

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
    
    def handle_cmp(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        self.alu("CMP", reg_1, reg_2)
        self.pc += 3

    def handle_jeq(self):
        if self.flag == 0b00000001:
            reg_index = self.ram[self.pc +1]
            self.pc = self.reg[reg_index]

            #  does same as the two lines above
            # self.pc = self.reg[self.ram[self.pc + 1]] # 2  self.reg at index 2

        else:
            self.pc += 2

    def handle_jmp(self):
        reg_index = self.ram[self.pc + 1]
        self.pc = self.reg[reg_index]
        

    def handle_jne(self):
        if self.flag != 0b00000001:
            reg_index = self.ram[self.pc + 1] # get the register reference number
            self.pc = self.reg[reg_index]
        
        else: self.pc += 2