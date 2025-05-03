# Ports
from utils import Port
CAMERA_PORT = Port((1180, 1190), (Port.Protocol.TCP, Port.Protocol.UDP))
SMARTDASHBOARD_PORT = Port(1735, Port.Protocol.TCP)
DASHBOARD_TO_ROBOT_CONTROL_PORT = Port(1130, Port.Protocol.UDP)
ROBOT_TO_DASHBOARD_CONTROL_PORT = Port(1140, Port.Protocol.UDP)
CAMERA_WEB_INTERFACE_PORT = Port(80, Port.Protocol.HTTP)
CAMERA_WEB_INTERFACE_SECURE_PORT = Port(443, Port.Protocol.HTTPS)
CAMERA_STREAMING_PORT = Port(554, (Port.Protocol.TCP, Port.Protocol.UDP))
CTRE_PORT = Port(1250, (Port.Protocol.TCP, Port.Protocol.UDP))
TEAM_USE_PORT = Port((5800, 5810), (Port.Protocol.TCP, Port.Protocol.UDP))

# IP Formats