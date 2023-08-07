"""Get IP info from ipinfo.io API."""
import os
import json
from urllib.request import urlopen


def get_ip_info(client_address):
    """Get IP info from ipinfo.io API."""
    url = f"https://ipinfo.io/{client_address}/json"
    token = os.environ.get("IPINFO_TOKEN", "")
    if token:
        url += f"?token={token}"
    response = urlopen(url)
    ip_info = json.load(response)
    return ip_info
