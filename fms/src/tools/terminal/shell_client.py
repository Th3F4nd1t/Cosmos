import socket
import sys

def main():
    HOST = "127.0.0.1"
    PORT = 9999

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)

    # Receive the initial greeting
    try:
        msg = s.recv(1024)
        if msg:
            print(msg.decode(), end="")
    except Exception:
        pass

    try:
        while True:
            cmd = input("> ").strip()
            if not cmd:
                continue
            s.sendall((cmd + "\n").encode())
            data = s.recv(1024)
            if not data:
                print("Disconnected from server.")
                break
            print(data.decode(), end="")
            if cmd.upper() == "QUIT":
                break
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
    finally:
        s.close()

if __name__ == "__main__":
    main()
