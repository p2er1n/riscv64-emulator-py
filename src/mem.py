class Mem:
    """
    """
    def __init__(self, size, start=0, init=0):
        self._start = start
        self._end = start + size - 1
        self._size = size
        self._mem = [init] * self._size 

    def read(self, start, size):
        return bytes(self._mem[start:start+size])

    def write(self, start, bts):
        for i in range(len(bts)):
            self._mem[start+i] = int(bts[i])

    def loadBin(self, path, start=0):
        with open(path, "rb") as f:
            bts = f.read()
            self.write(start, bts)
