from typing import Any


class NetworkHandler:
    def __init__(self):
        ...

    def send_udp(self, ip:str, port:int, data:Any) -> bool:
        ...