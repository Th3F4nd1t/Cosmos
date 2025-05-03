from enum import Enum




class Port:
    """A class that represents the data structure of a port. Should allow for ranges of ports to be reserved as well as the protocol."""

    class Protocol(Enum):
        TCP = 0
        UDP = 1
        HTTP = 2
        HTTPS = 3
        SSH = 4

    def __init__(self, port: int|Tuple[int, int], protocol: Protocol|Tuple[Protocol, Protocol]):
        if isinstance(port, tuple):
            self.port = port[0]
            self.start_port = port[0]
            self.end_port = port[1]
            self.spans = True
        else:
            self.port = port
            self.start_port = port
            self.end_port = port
            self.spans = False
            
        if isinstance(protocol, tuple):
            self.protocol = (protocol)
            self.multi_protocol = True
        elif isinstance(protocol, Protocol):
            self.protocol = protocol
            self.multi_protocol = False
        else:
            raise ValueError("Invalid protocol type. Must be Protocol or tuple of 2 Protocol.")

    def __str__(self):
        if self.spans:
            return f"port: {self.start_port}-{self.end_port}, protocol: {', '.join(p.name for p in self.protocol)}"
        return f"port: {self.port}, protocol: {self.protocol.name}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Port):
            return self.port == other.port and (self.spans != other.spans or (self.start_port == other.start_port and self.end_port == other.end_port)) and self.protocol == other.protocol
        return False