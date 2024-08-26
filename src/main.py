from hart import Hart
from mem import Mem
from utils.asm import asm

if __name__ == "__main__":
    mem = Mem(0x1000)
    mem.write(0x0,
              bytes(asm("addi", "x0", "x0", 1)) + 
              bytes(asm("addi", "x1", "x1", 2)) +
              bytes(asm("addi", "x2", "x2", 3)) +
              bytes(asm("addi", "x0", "x4", 666))
              )
    hart1 = Hart(mem)
    hart1.try_step()
    hart1.try_step()
    hart1.try_step()
    hart1.try_step()
