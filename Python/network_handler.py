from ds import Station
impr
class NetworkHandler:
    def __init__(self, 
                 network_adapter: str,
                 tcp: int=1750, 
                 udp_send: int=1120, 
                 udp_recv: int=1160, 
                 vlans=[10, 20, 30, 40, 50, 60],
                 fms_ip: str="10.0.100.5"):
        
        self.red_1_tcp_recv = []
        self.red_2_tcp_recv = []
        self.red_3_tcp_recv = []
        self.blue_1_tcp_recv = []
        self.blue_2_tcp_recv = []
        self.blue_3_tcp_recv = []

        self.red_1_udp_recv = []
        self.red_2_udp_recv = []
        self.red_3_udp_recv = []
        self.blue_1_udp_recv = []
        self.blue_2_udp_recv = []
        self.blue_3_udp_recv = []

    def start_tcp_recv(self):
        ...

    def start_udp_recv(self):
        ...

    def send_tcp(self, data: bytes, ip: str, station: int):
        ...

    def send_udp(self, data: bytes, ip: str, station: int):
        ...

    def stop_tcp_recv(self):
        ...

    def stop_udp_recv(self):
        ...

    def close(self):
        ...
        
    def is_new_tcp(self, station: Station):
        if station == Station.RED1:
            return len(self.red_1_tcp_recv) > 0
        elif station == Station.RED2:
            return len(self.red_2_tcp_recv) > 0
        elif station == Station.RED3:
            return len(self.red_3_tcp_recv) > 0
        elif station == Station.BLUE1:
            return len(self.blue_1_tcp_recv) > 0
        elif station == Station.BLUE2:
            return len(self.blue_2_tcp_recv) > 0
        elif station == Station.BLUE3:
            return len(self.blue_3_tcp_recv) > 0
        return False

    def get_tcp(self, station: Station):
        if station == Station.RED1:
            return self.red_1_tcp_recv.pop(0) if self.red_1_tcp_recv else None
        elif station == Station.RED2:
            return self.red_2_tcp_recv.pop(0) if self.red_2_tcp_recv else None
        elif station == Station.RED3:
            return self.red_3_tcp_recv.pop(0) if self.red_3_tcp_recv else None
        elif station == Station.BLUE1:
            return self.blue_1_tcp_recv.pop(0) if self.blue_1_tcp_recv else None
        elif station == Station.BLUE2:
            return self.blue_2_tcp_recv.pop(0) if self.blue_2_tcp_recv else None
        elif station == Station.BLUE3:
            return self.blue_3_tcp_recv.pop(0) if self.blue_3_tcp_recv else None
        return None
    
    def is_new_udp(self, station: Station):
        if station == Station.RED1:
            return len(self.red_1_udp_recv) > 0
        elif station == Station.RED2:
            return len(self.red_2_udp_recv) > 0
        elif station == Station.RED3:
            return len(self.red_3_udp_recv) > 0
        elif station == Station.BLUE1:
            return len(self.blue_1_udp_recv) > 0
        elif station == Station.BLUE2:
            return len(self.blue_2_udp_recv) > 0
        elif station == Station.BLUE3:
            return len(self.blue_3_udp_recv) > 0
        return False
    
    def get_udp(self, station: Station):
        if station == Station.RED1:
            return self.red_1_udp_recv.pop(0) if self.red_1_udp_recv else None
        elif station == Station.RED2:
            return self.red_2_udp_recv.pop(0) if self.red_2_udp_recv else None
        elif station == Station.RED3:
            return self.red_3_udp_recv.pop(0) if self.red_3_udp_recv else None
        elif station == Station.BLUE1:
            return self.blue_1_udp_recv.pop(0) if self.blue_1_udp_recv else None
        elif station == Station.BLUE2:
            return self.blue_2_udp_recv.pop(0) if self.blue_2_udp_recv else None
        elif station == Station.BLUE3:
            return self.blue_3_udp_recv.pop(0) if self.blue_3_udp_recv else None
        return None
        