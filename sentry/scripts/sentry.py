from sentry.send_serial import send_serial


def main():
    with open("cfg.txt") as f:
        config = f.read()
    send_serial(config)


if __name__ == "__main__":
    main()
