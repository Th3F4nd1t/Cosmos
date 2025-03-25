import socket
import threading

# Config
FMS_IP = "0.0.0.0"  # Listen on all network interfaces
FMS_UDP_PORT = 1160  # UDP Heartbeat
FMS_TCP_PORT = 1750  # TCP Match Control

def log(msg):
    print(f"[FMS] {msg}")

# === Fake FMS UDP Heartbeat Listener ===
def fms_udp_heartbeat():
    """Listens for DS heartbeats and responds to keep connection alive."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Fix for WinError 10048
    sock.bind((FMS_IP, FMS_UDP_PORT))
    log("Listening for Driver Station UDP heartbeats...")

    while True:
        data, addr = sock.recvfrom(1024)  # Receive DS heartbeat
        log(f"Heartbeat received from {addr}")

        # Send an FMS acknowledgment response
        sock.sendto(b"FMS_ACK", addr)
        log(f"Sent ACK to {addr}")

# === Fake FMS TCP Server ===
def fms_tcp_server():
    """Fakes an FMS TCP connection to the DS to make it think it's in an official match."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Fix for port reuse
    server.bind((FMS_IP, FMS_TCP_PORT))
    server.listen(5)
    log("Waiting for Driver Station TCP connection...")

    while True:
        conn, addr = server.accept()
        log(f"DS connected from {addr}")

        # Simulate FMS handshake
        conn.sendall(b"FMS_CONNECTED")
        log("Sent FMS connected status.")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            log(f"Received from DS: {data.decode()}")

        conn.close()
        log("DS disconnected.")

# === Start Threads ===
if __name__ == "__main__":
    log("Starting Fake FMS...")

    # Start UDP heartbeat listener
    udp_thread = threading.Thread(target=fms_udp_heartbeat, daemon=True)
    udp_thread.start()

    # Start TCP connection listener
    tcp_thread = threading.Thread(target=fms_tcp_server, daemon=True)
    tcp_thread.start()

    # Keep main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        log("Shutting down Fake FMS.")
