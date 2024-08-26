import time
from instr import Instr

RESET_VECTOR = 0x00_00_00_00_00_00_00_00
FREQUENCY = 10_000_000

DEBUG=True

class Register:
    def __init__(self, value):
        self.value = value

class CSR:
    pass

class Hart:
    """
    1. __init__, attach Mem and set reset vector
    2. try_step
    """
    def __init__(self, mem):
        self.mem = mem
        self._reset_vector = RESET_VECTOR
        self._frequency = FREQUENCY
        self._ipns = 1000_000_000 / self._frequency
        
        self._pc = Register(self._reset_vector)

        self.registers = [Register(0) for i in range(32)]
        self.x = self.registers
        
        self._last_step = time.perf_counter_ns()

    def try_step(self):
        self._curr_step = time.perf_counter_ns()
        duration = self._curr_step - self._last_step
        if duration < self._ipns:
            return False
        ret = self._execute()
        self._last_step = time.perf_counter_ns()
        return ret;

    def _execute(self):
        ir_bytes = self.mem.read(self._pc.value, 4)
        ir = Instr(ir_bytes)

        self._pc.value += 4
        ir.execute(self)

        if DEBUG:
            print("debug: " + "pc: " + str(self._pc.value) + " regs: " + ir.name + "\n" + str(self))
        
    def __str__(self):
        res = ""
        for r in self.x:
            res += str(r.value) + ", "
        res = res[:-1]
        return res
