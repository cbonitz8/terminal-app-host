from .app import TerminalAppHost


def main() -> None:
    app = TerminalAppHost()
    app.run()


if __name__ == "__main__":
    main()
