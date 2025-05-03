import paramiko

class SwitchHandler:
    """Handles the Cisco Catalyst 3850 and TP108E configuration for IPs and VLANs based on teams. Writes the configs to them."""
    def __init__(self):
        self.switches = {
            "center": {
                "ip": "...",
                "management_vlan": 1,
                "vlans": [10, 20, 30, 40, 50, 60],
                "ports": {
                    "red1": 1,
                    "red2": 2,
                    "red3": 3,
                    "blue1": 4,
                    "blue2": 5,
                    "blue3": 6
                }
            },
            "red_switch": {
                "ip": "...",
                "management_vlan": 1,
                "vlans": [10],
                "ports": {
                    "red1": 1,
                    "red2": 2,
                    "red3": 3
                }
            },
            "blue_switch": {
                "ip": "...",
                "management_vlan": 1,
                "vlans": [20],
                "ports": {
                    "blue1": 1,
                    "blue2": 2,
                    "blue3": 3
                }
            }
        }

        self.teams = [
            1,
            2,
            3,
            4,
            5,
            6,
        ]

        self.team_ips = {
            1: "10.0.1.5",
            2: "10.0.2.5",
            3: "10.0.3.5",
            4: "10.0.4.5",
            5: "10.0.5.5",
            6: "10.0.6.5",
        }

    def configure_switches(self):
        # Configure the center switch via SSH
        center_switch = self.switches["center"]
        ip = center_switch["ip"]
        username = "admin"  # Replace with actual username
        password = "password"  # Replace with actual password

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)

            for vlan in center_switch["vlans"]:
            command = f"vlan database\nvlan {vlan}\nexit"
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            print(stderr.read().decode())

            for port, port_number in center_switch["ports"].items():
            team_id = int(port[-1])  # Extract team ID from port name
            team_ip = self.team_ips[team_id]
            vlan = center_switch["vlans"][team_id - 1]
            command = f"interface GigabitEthernet0/{port_number}\nswitchport mode access\nswitchport access vlan {vlan}\nip address {team_ip} 255.255.255.0\nno shutdown\nexit"
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            print(stderr.read().decode())

            ssh.close()
        except Exception as e:
            print(f"Failed to configure center switch: {e}")

        # Configure the red switch via web interface(HTTP/HTTPS)


        # Configure the blue switch via web interface(HTTP/HTTPS)

