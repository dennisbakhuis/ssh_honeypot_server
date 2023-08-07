"""SSH Honeypot Server."""
import socket
import logging
import sys
import threading
from pathlib import Path
import argparse

import paramiko

from server.handle_ssh_connection import handle_ssh_connection


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()


def start_server(
    server_port: int = 2222,
    maximum_connections: int = 10,
    data_file_name: Path = Path("./ssh_honeypot_data.jsonl"),
):
    """Start the SSH Honeypot Server."""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("", server_port))
    except:
        logger.error("Failed to create and bind a new socket.")
        sys.exit(1)

    threads = []
    data_file_lock = threading.Lock()
    rsa_key = paramiko.RSAKey.generate(bits=2048)

    logger.info("Starting SSH Honeypot Server.")
    logger.info(f"Using port: {server_port}")
    logger.info(f"Using the following Data File: {data_file_name}")
    logger.info(f"Using maximum connections: {maximum_connections}")
    logger.info("Waiting for connections ...")

    while True:
        try:
            server_socket.listen(maximum_connections)
            client, address = server_socket.accept()
        except:
            logger.error(
                "Failed to create listen socket or accept the connection from the client.",
            )
            continue

        new_connection = threading.Thread(
            target=handle_ssh_connection,
            args=((client, address, rsa_key, data_file_name, data_file_lock)),
        )
        new_connection.start()
        threads.append(new_connection)

        for thread in threads:
            thread.join()


def main(arguments=None):
    """Parse aguments and starts the SSH Honeypot Server."""
    parser = argparse.ArgumentParser(
        description="SSH Honeypot Server.",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=2222,
        help="SSH server port (default: 2222)",
    )
    parser.add_argument(
        "-c",
        "--max-connections",
        type=int,
        default=10,
        help="Maximum number of simultaneous connections (default: 10)",
    )
    parser.add_argument(
        "-f",
        "--file",
        default="./ssh_honeypot_data.jsonl",
        help="Data file name (default: ./ssh_honeypot_data.jsonl)",
    )

    arguments = parser.parse_args(arguments)

    start_server(
        server_port=arguments.port,
        maximum_connections=arguments.max_connections,
        data_file_name=Path(arguments.file),
    )


if __name__ == "__main__":
    main()
