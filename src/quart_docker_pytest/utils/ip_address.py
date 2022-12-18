"""IP Address helpers."""
import ipaddress

import pyroute2


def find_bridge_gateway_ip() -> ipaddress.IPv4Address:
    """Finds the default gateway's IP address, used within Docker containers.

    The default gateway IP, or the bridge network IP address allows the Docker
    container to refer to the Docker host's IP address. Assumes the container
    only has one Docker network.
    """
    ndb = pyroute2.NDB()
    routes_summary = ndb.routes.summary()
    routes_summary.select_records(
        gateway=lambda g: bool(g),
        ifname=lambda i: i == "eth0",
        target=lambda t: t == "localhost",
    )

    routes = list(routes_summary)
    route = routes[0]

    return ipaddress.IPv4Address(route.gateway)


def find_bridge_gateway_subnet_range() -> ipaddress.IPv4Network:
    """Find the default gateway's subnet range.

    The default gateway's subnet range is helpful for Home Assistant's
    "trusted_proxies" config property. Assumes the container only has one
    Docker network.
    """
    ndb = pyroute2.NDB()
    eth0 = ndb.interfaces["eth0"]
    container_ip = eth0.ipaddr.summary()[0]
    gateway_ip = str(find_bridge_gateway_ip())
    subnet_ip = ".".join([*gateway_ip.split(".")[:-1], "0"])

    return ipaddress.IPv4Network((subnet_ip, container_ip.prefixlen))
