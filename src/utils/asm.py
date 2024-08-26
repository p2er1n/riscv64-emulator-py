from .bits import Bits

INSTRs = {
    "add": { "type": 'r', "opcode": 0b0110011, "funct3": 0x0, "funct7": 0x00 },
    "sub": { "type": 'r', "opcode": 0b0110011, "funct3": 0x0, "funct7": 0x20 },

    "addi": { "type": 'i', "opcode": 0b0010011, "funct3": 0x0},
}

REGs = {}
for i in range(32):
    name = "x" + str(i)
    REGs[name] = i

def asm(name, operand1, operand2, operand3=0):
    """
    Examples: asm("addi", "x0", "x0", 100)
    """
    if name not in INSTRs:
        return

    detail = INSTRs[name]
    tp = detail["type"]
    if tp == "r":
        rd = REGs[operand1]
        rs1 = REGs[operand2]
        rs2 = REGs[operand3]
        res = _asm_r(detail["opcode"], rd, detail["funct3"], rs1, rs2, detail["funct7"])
    elif tp == "i":
        rd = REGs[operand1]
        rs1 = REGs[operand2]
        imm = operand3
        res = _asm_i(detail["opcode"], rd, detail["funct3"], rs1, imm)
    else:
        pass
    
    return res

def _asm_i(opcode, rd, funct3, rs1, imm):
    ir = Bits(b"\x00\x00\x00\x00")
    idx = 0
    
    opcode = Bits(opcode.to_bytes())
    for i in range(7):
        ir[idx+i] = opcode[i]
    idx += 7

    rd = Bits(rd.to_bytes())
    for i in range(5):
        ir[idx+i] = rd[i]
    idx += 5

    funct3 = Bits(funct3.to_bytes())
    for i in range(3):
        ir[idx+i] = funct3[i]
    idx += 3

    rs1 = Bits(rs1.to_bytes())
    for i in range(5):
        ir[idx+i] = rs1[i]
    idx += 5

    imm = Bits(imm.to_bytes(2, signed=True, byteorder="little"))
    for i in range(12):
        ir[idx+i] = imm[i]
    idx+= 12
    
    return ir

def _asm_r(opcode, rd, funct3, rs1, rs2, funct7):
    ir = Bits(b"\x00\x00\x00\x00")
    idx = 0
    
    opcode = Bits(opcode.to_bytes())
    for i in range(7):
        ir[idx+i] = opcode[i]
    idx += 7

    rd = Bits(rd.to_bytes())
    for i in range(5):
        ir[idx+i] = rd[i]
    idx += 5

    funct3 = Bits(funct3.to_bytes())
    for i in range(3):
        ir[idx+i] = funct3[i]
    idx += 3

    rs1 = Bits(rs1.to_bytes())
    for i in range(5):
        ir[idx+i] = rs1[i]
    idx += 5

    rs2 = Bits(rs2.to_bytes())
    for i in range(5):
        ir[idx+i] = rs2[i]
    idx += 5

    funct7 = Bits(funct7.to_bytes())
    for i in range(7):
        ir[idx+i] = funct7[i]
    idx += 7

    return ir
