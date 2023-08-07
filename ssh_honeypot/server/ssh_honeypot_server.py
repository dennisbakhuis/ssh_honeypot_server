"""Implements a SSH server interface for the honeypot."""
import threading
import datetime
import json
import logging
from pathlib import Path

import paramiko

from .get_ip_info import get_ip_info


logger = logging.getLogger()


class SSHHoneypotServer(paramiko.ServerInterface):
    """
    Implements a SSH server interface for the honeypot.

    This interface will be started each time a client connects to the honeypot.
    """

    def __init__(
        self,
        address,
        data_file_name: Path,
        data_file_lock: threading.Lock,
        ip_info_api_token: str,
    ):
        """
        Create a new SSH server interface.

        Parameters
        ----------
        address
            The client address.
        data_file_name : Path
            The data file name.
        data_file_lock : threading.Lock
            The data file lock.
        """
        self.event = threading.Event()
        self.client_address = address
        self.data_file_name = data_file_name
        self.data_file_lock = data_file_lock
        self.ip_info_api_token = ip_info_api_token

    def check_channel_request(self, kind, chanid):
        """Check the channel request."""
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED  # type: ignore

        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED  # type: ignore

    def check_auth_password(self, username, password):
        """
        Mock the authentication process and logs credentials and IP info.

        Authentication is always failed.

        Parameters
        ----------
        username : str
            The username.
        password : str
            The password.
        """
        self.data_file_lock.acquire()

        try:
            log_file = open(self.data_file_name, "a")
            ip_info = get_ip_info(self.client_address[0], self.ip_info_api_token)
            row = {
                "timestamp": datetime.datetime.now().isoformat(" ", "seconds"),
                "username": username,
                "password": password,
                **ip_info,
            }
            log_file.write(f"{json.dumps(row)}\n")
            log_file.close()

            logger.info(
                f"New connection from {self.client_address[0]} trying to login with {username}:{password}."
            )
        finally:
            self.data_file_lock.release()

        return paramiko.AUTH_FAILED  # type: ignore
