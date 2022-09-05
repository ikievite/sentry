"""Send commands to device."""


import logging
import sys
import time

import serial

logger = logging.getLogger(__name__)

port = "/dev/ttyUSB0"
bps = 9600

READ_TIMEOUT = 8


def to_bytes(line=""):
    """
    Convert line to bytes.

    Args:
        line: text line

    Returns:
        bytes line
    """
    return f"{line}\n".encode("utf-8")


def read_serial(console):
    """
    Check if there is data waiting to be read. Read and return it, else return null string.

    Args:
        console: console connection

    Returns:
        data waiting to be read
    """
    data_bytes = console.in_waiting
    if data_bytes:
        return console.read(data_bytes)
    return ""


def check_logged_in(console):
    """
    Check if logged in to switch.

    Args:
        console: console connection

    Returns:
        status is logged
    """
    console.write(to_bytes("\n"))
    time.sleep(1)
    prompt = read_serial(console)
    if b">" in prompt or b"#" in prompt:
        return True
    return False


def login(console):
    """
    Login to switch.

    Args:
        console: console connection
    """
    login_status = check_logged_in(console)
    if login_status:
        logger.debug("Already logged in")
        return None

    logger.debug("Logging into switch")
    while True:
        console.write(to_bytes())
        time.sleep(1)
        input_data = read_serial(console)
        if not b"Login" in input_data:
            continue
        console.write(to_bytes("raisecom"))
        time.sleep(1)
        input_data = read_serial(console)
        if not b"Password" in input_data:
            continue
        console.write(to_bytes("raisecom"))
        time.sleep(1)

        login_status = check_logged_in(console)
        if login_status:
            logger.debug("We are logged in")
            break


def logout(console):
    """
    Exit from console session.

    Args:
        console: console connection
    """
    logger.debug("Logging out from switch")
    while check_logged_in(console):
        console.write(to_bytes("exit"))
        time.sleep(0.5)

    logger.debug("Successfully logged out from switch")


def send_command(console, cmd=""):
    """
    Send a command down the channel.

    Args:
        console: console connection
        cmd: command`s string

    Returns:
        applied command

    Return the output
    """
    console.write(to_bytes(cmd))
    time.sleep(1)
    return read_serial(console).decode("utf-8")


def send_serial(config):
    """
    Send commands to device via serial port.

    Args:
        config: device`s commands
    """
    logger.debug("Initializing serial connection")

    console = serial.Serial(
        port=port,
        baudrate=bps,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=READ_TIMEOUT,
    )

    if not console.is_open:
        sys.exit()

    login(console)
    for line in config.split("\n"):
        logger.debug(send_command(console, cmd=line))

    logout(console)
