import socket
import threading
import struct
import time

# Constants
FMS_TCP_PORT = 1750
FMS_UDP_PORT_DS = 1121  # FMS -> DS (Control Packets)
FMS_UDP_PORT_FMS = 1160  # DS -> FMS (Status Packets)

# Tracking connected Driver Stations
ds_clients = {}

# Function to handle DS connection over TCP
def handle_ds_connection(conn, addr):
    print(f"[INFO] Driver Station connected from {addr}")
    ds_clients[addr] = conn
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[DS] Received: {data.hex()}")
            
            # Simulated FMS response packet (modify as needed)
            fms_response = struct.pack('BBBB', 0x01, 0x02, 0x03, 0x04)
            conn.sendall(fms_response)
            print(f"[FMS] Sent: {fms_response.hex()}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        del ds_clients[addr]
        print(f"[INFO] Driver Station {addr} disconnected")

# UDP Listener for DS -> FMS packets (Status updates)
def listen_ds_status():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", FMS_UDP_PORT_FMS))
    print(f"[INFO] Listening for DS status packets on UDP {FMS_UDP_PORT_FMS}")
    
    while True:
        data, addr = udp_socket.recvfrom(50)
        if len(data) >= 8:
            team_id = struct.unpack('>H', data[4:6])[0]
            battery_voltage = struct.unpack('>H', data[6:8])[0] / 256.0
            print(f"[DS] Status from {addr} - Team {team_id}, Battery: {battery_voltage:.2f}V")

# Function to send control packets to DS
def send_control_packet(ds_ip, alliance_station, match_type, match_number, match_time):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = struct.pack(
        '>HBBBxBHHBx6BHH',
        0x0001,  # Packet count
        0x00,    # Protocol version
        0x04,    # Status flags (Enabled example)
        0x00,    # Unused
        alliance_station,
        match_type,
        match_number,
        1,  # Match repeat number
        *time.gmtime()[0:6],  # Timestamp
        match_time  # Match time remaining
    )
    udp_socket.sendto(packet, (ds_ip, FMS_UDP_PORT_DS))
    print(f"[FMS] Sent control packet to {ds_ip}")

# TCP Server to accept DS connections
def start_fms_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", FMS_TCP_PORT))
        server.listen(5)
        print(f"[INFO] FMS server running on TCP {FMS_TCP_PORT}")
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_ds_connection, args=(conn, addr))
            thread.start()

# Start all threads
if __name__ == "__main__":
    threading.Thread(target=start_fms_server, daemon=True).start()
    threading.Thread(target=listen_ds_status, daemon=True).start()
    
    while True:
        time.sleep(10)  # Keep main thread alive
