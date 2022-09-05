import serial

from sentry.send_serial import (
    READ_TIMEOUT,
    bps,
    login,
    logout,
    port,
    send_command,
    send_serial,
)


def test_send_serial():
    config = """!
    hostname test1234
    !"""
    send_serial(config)
    console = serial.Serial(
        port=port,
        baudrate=bps,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=READ_TIMEOUT,
    )
    login(console)
    received = send_command(console, "show clock")
    logout(console)
    assert "test1234" in str(received)
