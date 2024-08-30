from hart import Hart
from mem import Mem
from utils.asm import asm

if __name__ == "__main__":
    mem = Mem(m_size=2**20*100)
    mem.loadBytes(
        bytes(asm("addi","x0","x0",1)) +
        bytes(asm("addi","x1","x1",1)) +
        bytes(asm("add","x0","x0","x1"))
                  )
    hart1 = Hart(mem)
    hart1.try_step()
    hart1.try_step()
    hart1.try_step()
