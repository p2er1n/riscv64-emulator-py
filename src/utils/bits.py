class Bits:
    """
    little-endian encoding
    """

    def __init__(self, bs):
        if isinstance(bs, list):
            self._length = len(bs)
            self._array = bs[0:]
        else:
            self._length = len(bs) * 8
            self._array = []
            for b in bs:
                for i in range(8):
                    self._array.append((b >> i) & 0b1)
                
    def __getitem__(self, index):
        if isinstance(index, int):
            return self._array[index]
        else:
            start = index.start
            stop = index.stop
            if start is None:
                start = 0
            if stop is None:
                stop = self._length
            return Bits(self._array[start : stop])
        
    def __setitem__(self, index, value):
        self._array[index] = value

    def __len__(self):
        return self._length
    
    def __bytes__(self):
        bs = b""
        for i in range(0, self._length, 8):
            bt = 0
            for j in range(0, 8):
                bt += self._array[i+j] * 2**j
            bs += bt.to_bytes()
        return bs

    def __str__(self):
        s = ""
        for i in range(self._length):
            s += str(self._array[i])
        return s

    def to_int(self):
        return int(str(self)[::-1], 2)

    def to_signed_int(self):
        res = 0
        for i in range(self._length-1):
            res += 2**i * self._array[i]
        res += -(2**(self._length-1)) * self._array[self._length-1]
        return res
