from netmiko import ConnectHandler
from tools.terminal.decorators import user_run, system_run

class SwitchConfig:
    @system_run
    def __init__(self, config_file: str):
        self.config_file = config_file

        self.lines = []

        for line in open(config_file, 'r'):
            self.lines.append(line)
        ...

    @system_run
    def parse_config(self, fms):
        """
        Syntax:
        <&station_1@team_number>
        <&station_1@team_name>
        <&station_1@ip>

        <&plc_red@ip>
        <&plc_blue@ip>

        Then return the string with the parsed values.
        """
        
        parsed_lines = []

        for line in self.lines:
            # check if line contains a token (a <& or <$ and also a >)
            if '<&' in line or '<$' in line:
                # Parse the line for tokens
                parsed_line = self._parse_line(line, fms)
                parsed_lines.append(parsed_line)
            else:
                # If no tokens, just append the line as is
                parsed_lines.append(line)

        return ''.join(parsed_lines)
    
    @system_run
    def _parse_line(self, line: str, fms):
        """
        Parses a single line, replacing tokens with actual values from the fms object.
        Supports:
        - <$mode=...> for the match mode.
        - <&station_1@team_number>, etc. for station/team properties.
        - <&plc_red@ip> or similar for PLC data.
        """

        import re

        # First handle <$...> tokens
        @system_run
        def parse_mode_token(match):
            token = match.group(1)
            if token.startswith('mode='):
                mode_value = token[5:]  # Strip 'mode='
                # Let’s pretend fms has a method get_mode_value(mode)
                try:
                    return fms.get_mode_value(mode_value)
                except AttributeError:
                    raise ValueError(f"fms object has no 'get_mode_value' method. Fix your mess.")
            else:
                raise ValueError(f"Unknown <$...> token: '{token}'")

        line = re.sub(r'<\$(.*?)>', parse_mode_token, line)

        # Next handle <&...> tokens
        @system_run
        def parse_data_token(match):
            token = match.group(1)
            if '@' not in token:
                raise ValueError(f"Invalid token format: '{token}' (expected '@' separator)")

            key, attribute = token.split('@', 1)
            # Handle station_1, station_2, etc.
            if key.startswith('station_'):
                station = key.split('_')[1]
                try:
                    station_obj = fms.get_station(int(station))
                except AttributeError:
                    raise ValueError(f"fms object has no 'get_station' method. Seriously?")
                value = getattr(station_obj, attribute, None)
                if value is None:
                    raise ValueError(f"Attribute '{attribute}' not found on station {station}. Sucks to be you.")
                return str(value)
            elif key.startswith('plc_'):
                plc_color = key.split('_')[1]
                try:
                    plc_obj = fms.get_plc(plc_color)
                except AttributeError:
                    raise ValueError(f"fms object has no 'get_plc' method. This is getting ridiculous.")
                value = getattr(plc_obj, attribute, None)
                if value is None:
                    raise ValueError(f"Attribute '{attribute}' not found on PLC '{plc_color}'.")
                return str(value)
            else:
                raise ValueError(f"Unknown key in token: '{key}'")

        line = re.sub(r'<&(.*?)>', parse_data_token, line)

        return line
    
    @system_run
    def write_to_switch(self, ip: str, username: str, password: str):
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }

        with ConnectHandler(**device) as net_connect:
            for line in self.lines:
                if line.strip():
                    net_connect.send_config_set(line.strip())




class MainSwitchConfig(SwitchConfig):
    ...



class RedSwitchConfig(SwitchConfig):
    ...



class BlueSwitchConfig(SwitchConfig):
    ...