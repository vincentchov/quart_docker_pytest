"""Caddy Helpers."""
import os

from jinja2 import Environment
from jinja2 import FileSystemLoader

from quart_docker_pytest.utils import ip_address


def init_caddy() -> None:
    """Initializes Caddyfile necessary for Caddy service to run.

    Fills out a Caddyfile Jinja2 template and outputs the file for Caddy to
    use.  On the first run, Caddy will lack a Caddyfile and should continue to
    restart until this function is done creating the Caddyfile.
    """
    loader = FileSystemLoader("/app/reverse_proxy_tmpl")
    env = Environment(loader=loader, autoescape=True)
    template = env.get_template("Caddyfile.tmpl")
    template.environment.trim_blocks = True
    template.environment.lstrip_blocks = True

    jinja_vars = {
        "BRIDGE_GATEWAY_IP": str(ip_address.find_bridge_gateway_ip()),
        "BASE_DOMAIN": os.getenv("BASE_DOMAIN"),
        "CADDY_USE_WILDCARDS": bool(os.getenv("CADDY_USE_WILDCARDS", 0)),
        "LETSENCRYPT_EMAIL": os.getenv("LETSENCRYPT_EMAIL"),
        "PRE_EXISTING_CERT_PATH": os.getenv("PRE_EXISTING_CERT_PATH"),
        "PRE_EXISTING_CERT_KEY_PATH": os.getenv("PRE_EXISTING_CERT_KEY_PATH"),
    }
    caddyfile_templated = template.render(jinja_vars)
    with open("/app/reverse_proxy_tmpl/Caddyfile", "w") as caddyfile:
        caddyfile.write(caddyfile_templated)
