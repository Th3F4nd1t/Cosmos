class IP:
    def __init__(self, ip: str, mask: str):
        self.ip = ip
        self.mask = mask

class TeamIP(IP):
    def __init__(self, fmat: str, team: int, mask: str):
        self.team = team
        self.fmat = fmat

        # Split the format into parts
        parts = fmat.split()

        # Identify positions of 'x', right to left
        x_positions = [i for i in reversed(range(len(parts))) if parts[i] == 'x']
        print(x_positions)
        # Fill in the 'x' placeholders with team number bytes (right to left)
        for pos in x_positions:
            parts[pos] = str(team % 256)
            team //= 256

        ip_address = '.'.join(parts)
        super().__init__(ip_address, mask)



if __name__ == "__main__":
    # Example usage
    team_ip = TeamIP("10.xxx.xx.5", 123, "255.255.255.0")
    print(f"Team IP: {team_ip.ip}, Mask: {team_ip.mask}")