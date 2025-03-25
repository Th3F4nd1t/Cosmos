import requests

class FieldAP:
    def __init__(self, ip):
        self.ip = ip
    
    def get_status(self):
        try:
            response = requests.get(f"http://{self.ip}/status")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching AP status: {e}")
            return None
        
    def configure(self, channel, red_vlans, blue_vlans, station_configs):
        config_data = {
            "channel": channel,
            "redVlans": red_vlans,
            "blueVlans": blue_vlans,
            "stationConfigurations": station_configs
        }

        try:
            response = requests.post(f"http://{self.ip}/configuration", json=config_data)
            response.raise_for_status()
            if response.status_code == 202:
                print("Configuration successful!")
            else:
                print(f"Unexpected response: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error configuring AP: {e}")

    def display_connections(self):
        status = self.get_status()
        if not status:
            return
        
        print("\n--- Current Connections ---")
        for station, details in status.get("stationStatuses", {}).items():
            if details:
                print(f"{station.capitalize()}: {details.get('macAddress', 'N/A')}")
                print(f"  Linked: {details.get('isLinked', 'N/A')}")
                print(f"  Rx Rate: {details.get('rxRateMbps', 'N/A')} Mbps")
                print(f"  Bandwidth: {details.get('bandwidthUsedMbps', 'N/A')} Mbps")
                print(f"  Quality: {details.get('connectionQuality', 'N/A')}")
            else:
                print(f"{station.capitalize()}: No data available.")