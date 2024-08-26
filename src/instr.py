from utils.bits import Bits

R_OPCODE = 0b011_0011
I_OPCODEs = [ 0b001_0011, 0b000_0011, 0b110_0111, 0b111_0011 ]
S_OPCODE = 0b010_0011
B_OPCODE = 0b110_0011
J_OPCODE = 0b110_1111
U_OPCODEs = [ 0b011_0111, 0b001_0111 ]

class Instr:
    """
    little-endian decoding
    """

    def _add(self, hart):
        hart.x[self._rd].value = hart.x[self._rs1].value + hart.x[self._rs2].value

    def _sub(self, hart):
        hart.x[self._rd].value = hart.x[self._rs1].value - hart.x[self._rs2].value

    def _addi(self, hart):
        hart.x[self._rd].value = hart.x[self._rs1].value + self._imm_raw.to_signed_int()
        
    def execute(self, hart):
        mapping = {
            'add': self._add,
            'addi': self._addi,
            # todo
        }
        return mapping[self.name](hart)
    
    def _parse(self):
        self._opcode = self._bits[0:7].to_int()

        if self._opcode == R_OPCODE:
            self._r_parse()
        elif self._opcode in I_OPCODEs:
            self._i_parse()
        elif self._opcode == S_OPCODE:
            self._s_parse()
        elif self._opcode == B_OPCODE:
            self._b_parse()
        elif self._opcode == J_OPCODE:
            self._j_parse()
        elif self._opcode in U_OPCODEs:
            self._u_parse()
        else:
            pass
        
    def _r_parse(self):
        self._rd = self._bits[7:12].to_int()
        self._funct3 = self._bits[12:15].to_int()
        self._rs1 = self._bits[15:20].to_int()
        self._rs2 = self._bits[20:25].to_int()
        self._funct7 = self._bits[25:32].to_int()

        if self._funct3 == 0x0:
            if self._funct7 == 0x00:
                self.name = "add"
            elif self._funct7 == 0x20:
                self.name = "sub"
        elif self._funct3 == 0x4 and self._funct7 == 0x00:
            self.name = "xor"
        else:
            pass # wrong instruction

    def _i_parse(self):
        self._rd = self._bits[7:12].to_int()
        self._funct3 = self._bits[12:15].to_int()
        self._rs1 = self._bits[15:20].to_int()
        self._imm_raw = self._bits[20:32]

        if self._opcode == 0b0010011:
            if self._funct3 == 0x0:
                self.name = "addi"
            elif self._funct3 == 0x4:
                self.name = "xori"
            elif self._funct3 == 0x6:
                self.name = "ori"
            elif self._funct3 == 0x7:
                self.name = "andi"
            else:
                pass #todo
        elif self._opcode == 0b0000011:
            pass
        elif self._opcode == 0b1100111:
            pass
        elif self._opcode == 0b1110011:
            pass
        else:
            pass # wrong instruction

    def _s_parse(self):
        pass
    def _b_parse(self):
        pass
    def _j_parse(self):
        pass
    def _u_parse(self):
        pass
    
    def __init__(self, bs):
        # parse bs to get instruction name, registers and immediates
        self._bits = Bits(bs)
        self._parse()
