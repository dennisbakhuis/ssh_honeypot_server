"""Get IP info from ipinfo.io API."""
import os
import json
from urllib.request import urlopen


def get_ip_info(client_address, ip_info_api_token):
    """Get IP info from ipinfo.io API."""
    url = f"https://ipinfo.io/{client_address}/json"
    if ip_info_api_token:
        url += f"?token={ip_info_api_token}"
    response = urlopen(url)
    ip_info = json.load(response)
    return ip_info
