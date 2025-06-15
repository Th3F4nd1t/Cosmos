from typing import Any
from tools.terminal.decorators import user_run, system_run


class NetworkHandler:
    @system_run
    def __init__(self):
        ...

    @system_run
    def send_udp(self, ip:str, port:int, data:Any) -> bool:
        ...