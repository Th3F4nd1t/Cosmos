from enum import Enum
import socket
import threading

from core.eventbus.events import GeneralEvent



class SocketServer:
    def __init__(self, fms, bind_addr:str="127.0.0.1", bind_port:int=9999):
        self.fms = fms
        self.bind_addr = bind_addr
        self.bind_port = bind_port
        self.client_ids = []
        self.clients = []

    def get_next_client_id(self) -> int:
        if not self.client_ids:
            self.client_ids.append(1)
            return 1
        else:
            self.client_ids.append(max(self.client_ids) + 1)
            return max(self.client_ids)

    def run(self):
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.srv.bind((self.bind_addr, self.bind_port))
            self.srv.listen(5)
            self.fms.emit(GeneralEvent.DEBUG, {"message": f"Socket server listening on {self.bind_addr}:{self.bind_port}"})
            while True:
                conn, addr = self.srv.accept()
                self.clients.append(conn)
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

        except Exception as e:
            self.fms.emit(GeneralEvent.ERROR, {"message": f"Socket server error: {e}"})

        finally:
            try:
                self.srv.close()
                self.client_ids.clear()
                self.clients.clear()
            except Exception:
                pass

    def handle_client(self, conn, addr):
        client_id = self.get_next_client_id()
        conn.sendall(f"Connected to Cosmos FMS socket server with client ID {client_id}. For help, type HELP\n".encode())

        try:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                cmd = data.split(" ")

                if cmd[0].lower() == "quit":
                    conn.sendall("Exiting...\n".encode())
                    break

                elif cmd[0].lower() == "pin":
                    if len(cmd) < 2:
                        self.send_response(conn, "Invalid pin command")
                        continue

                    if cmd[1].lower() == "set":
                        if len(cmd) < 3:
                            self.send_response(conn, "Usage: PIN SET <value>")
                            continue
                        pin_value = cmd[2]
                        if self.fms.pin is None:
                            self.fms.pin = pin_value
                            self.send_response(conn, "Success")
                        else:
                            self.send_response(conn, "Pin already set")

                    elif cmd[1].lower() == "get":
                        is_set = self.fms.pin is not None
                        self.send_response(conn, "true" if is_set else "false")

                    else:
                        self.send_response(conn, "Invalid PIN subcommand")

                elif cmd[0].lower() == "turn":
                    if len(cmd) < 3:
                        self.send_response(conn, "Invalid turn command")
                        continue

                    # turn <on|off> <pin>
                    action = cmd[1].lower()
                    pin_value = cmd[2]

                    if self.fms.pin is None:
                        self.send_response(conn, "Pin not set. Use `pin set <value>` to set the pin first.")
                        continue
                    if pin_value != self.fms.pin:
                        self.send_response(conn, "Invalid pin")
                        continue

                    if action == "on":
                        self.fms.turn_on = True
                        self.send_response(conn, "FMS turning on")

                    elif action == "off":
                        self.fms.turn_off = True
                        self.send_response(conn, "FMS turning off")

                    else:
                        self.send_response(conn, "Invalid TURN subcommand")

                elif cmd[0].lower() == "mode":
                    self.send_response(conn, f"Current mode: {self.fms.mode.__class__.__name__}")

                else:
                    self.send_response(conn, "Unknown command. Type HELP for a list of commands.")

        except ConnectionResetError:
            print(f"Client {addr} disconnected abruptly.")
        finally:
            conn.close()


    def send_response(self, client_socket, response:str):
        client_socket.sendall(f"{response}\n".encode())

    def broadcast(self, message:str):
        for client in self.clients:
            self.send_response(client, message)