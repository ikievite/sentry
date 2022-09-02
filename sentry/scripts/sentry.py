"""Send commands to device via serial port."""


from sentry.send_serial import send_serial


def main():
    """Run main function."""
    with open("cfg.txt") as f:
        config = f.read()
    send_serial(config)


if __name__ == "__main__":
    main()
