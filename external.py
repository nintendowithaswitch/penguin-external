import time
import sys
from penguin_external.penguin import Penguin
from penguin_external.server import start_server
from penguin_external.launcher import launch_overlay


def main():
    port = 1337

    penguin = Penguin()
    penguin.start()

    server = start_server(port, penguin)

    print("[penguin] starting overlay...")
    time.sleep(0.4)
    launch_overlay(f"http://localhost:{port}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        penguin.stop()
        try:
            server.shutdown()
        except Exception:
            pass
        print("\n[penguin] stopped — goodbye")
        sys.exit(0)


if __name__ == "__main__":
    main()