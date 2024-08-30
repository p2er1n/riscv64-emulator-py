class Mem:
    """
    """
    def __init__(self, m_start=0x0, m_size=100*2**20):
        self._map = [
            {"type": "RAM", "range": [m_start, m_start+m_size-1], "content": [0] * m_size},
        ]

    def _ram_map(self, rg, content):
        self._map.append({
            "type": "RAM",
            "range": rg[:],
            "content": content
        })

    def _rom_map(self, rg, content):
        self._map.append({
            "type": "ROM",
            "range": rg[:],
            "content": content
        })
        
    def _io_map(self, rg, registers, callback): # <fixme>
        self._map.append({
            "type": "IO",
            "range": rg[:],
            "registers": registers,
            "callback": callback
        })
        
    def map(self, tp, rg, value):
        if tp == "RAM":
            _ram_map(rg, value)
        elif tp == "ROM":
            _rom_map(rg, value)
        elif tp == "IO":
            _io_map(rg, value["registers"], value["callback"])
        else:
            pass # unreachable
    
    def read(self, pos):
        for space in self._map:
            if pos >= space["range"][0] and pos <= space["range"][1]:
                return space["content"][pos - space["range"][0]]

    def readBytes(self, start, size):
        res = []
        for pos in range(start, start+size):
            res.append(self.read(pos))
        return bytes(res)
            
    def write(self, start, b):
        for space in self._map:
            if space["type"] == "ROM":
                continue
            elif space["type"] == "RAM":
                if pos >= space["range"][0] and pos <= space["range"][1]:
                    space["content"][pos - space["range"][0]] = b
                    break
            elif space["type"] == "IO":
                if pos >= space["range"][0] and pos <= space["range"][1]:
                    old_b = space["registers"][pos- space["range"][0]]
                    space["registers"][pos- space["range"][0]] = b
                    space["callback"](registers, pos, old_b, b)
                    break
                
    def loadBin(self, path, start=0):
        with open("path", "rb") as f:
            bs = f.read()
            for space in self._map:
                if start >= space["range"][0] and start+len(bs)-1 <= space["range"][1]:
                    if space["type"] == "IO":
                        continue # cannot load bytes into IO registers
                    space["content"][start - space["range"][0]: start - space["range"][0] + len(bs)] = bs
                    break

    def loadBytes(self, bs, start=0):
        for space in self._map:
            if start >= space["range"][0] and start+len(bs)-1 <= space["range"][1]:
                if space["type"] == "IO":
                    continue # cannot load bytes into IO registers
                space["content"][start - space["range"][0]: start - space["range"][0] + len(bs)] = bs
                break
        
