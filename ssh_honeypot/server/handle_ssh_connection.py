"""Handles a new SSH connection."""
import logging
import threading
from pathlib import Path

import paramiko

from .ssh_honeypot_server import SSHHoneypotServer


logger = logging.getLogger()


def handle_ssh_connection(
    client,
    address,
    rsa_key,
    data_file_name: Path,
    data_file_lock: threading.Lock,
):
    """Handle a new SSH connection."""
    try:
        transport = paramiko.Transport(client)

        transport.add_server_key(rsa_key)
        server = SSHHoneypotServer(address, data_file_name, data_file_lock)

        try:
            transport.start_server(server=server)
        except:
            logging.error("Error: SSH Negotation failed.")
            return

        channel = transport.accept(20)

        if channel is None:
            transport.close()
            return

        server.event.wait()

        if not server.event.is_set():
            transport.close()
            return

        channel.close()

    except:
        logger.error("Error: Could not generate a new connection.")
        transport.close()  # type: ignore
