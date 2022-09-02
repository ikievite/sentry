"""Send commands to device."""


import sys
import time

import serial

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
    else:
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
    else:
        return False


def login(console):
    """
    Login to switch.

    Args:
        console: console connection
    """
    login_status = check_logged_in(console)
    if login_status:
        print("Already logged in")
        return None

    print("Logging into switch")
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
            print("We are logged in\n")
            break


def logout(console):
    """
    Exit from console session.

    Args:
        console: console connection
    """
    print("Logging out from switch")
    while check_logged_in(console):
        console.write(to_bytes("exit"))
        time.sleep(0.5)

    print("Successfully logged out from switcc")


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
    print("\nInitializing serial connection")

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
        print(send_command(console, cmd=line))

    logout(console)
