from typing import Callable


class Route:
    gateway: str
    ifname: str
    target: str

class RoutesView(list[Route]):
    def summary(self) -> RoutesView: ...
    def select_records(
        self,
        gateway: Callable[[str], bool] = lambda g: True,
        ifname: Callable[[str], bool] = lambda i: True,
        target: Callable[[str], bool] = lambda t: True,
    ) -> None: ...

class NetworkInterface:
    ipaddr: IPAddrView

class IPAddr(str):
    prefixlen: int

class IPAddrView:
    def summary(self) -> list[IPAddr]: ...
    def select_records(
        self,
        address: Callable[[str], bool] = lambda a: True,
        target: Callable[[str], bool] = lambda t: True,
    ) -> None: ...

class NDB:
    routes: RoutesView
    interfaces: dict[str, NetworkInterface]
