import pyautogui
import time

# Delay before starting so you can ALT+TAB into PuTTY or whatever you're doing
print("You have 5 seconds to focus the PuTTY window. Hurry up.")
time.sleep(5)

config_commands = [
    "vlan 10",
    " name Red1",
    "exit",
    "vlan 20",
    " name Red2",
    "exit",
    "vlan 30",
    " name Red3",
    "exit",
    "vlan 40",
    " name Blue1",
    "exit",
    "vlan 50",
    " name Blue2",
    "exit",
    "vlan 60",
    " name Blue3",
    "exit",
    "vlan 100",
    " name CosmosMgmt",
    "exit",

    "interface GigabitEthernet1/0/1",
    " description Red Alliance Switch",
    " switchport mode trunk",
    " switchport trunk allowed vlan 10,20,30,100",
    "exit",

    "interface GigabitEthernet1/0/3",
    " description Blue Alliance Switch",
    " switchport mode trunk",
    " switchport trunk allowed vlan 40,50,60,100",
    "exit",

    "interface GigabitEthernet1/0/13",
    " description Field AP (All VLANs)",
    " switchport mode trunk",
    " switchport trunk allowed vlan 10,20,30,40,50,60,100",
    "exit",

    "interface GigabitEthernet1/0/15",
    " description Field WiFi (Mgmt Only)",
    " switchport mode access",
    " switchport access vlan 100",
    "exit",

    "interface GigabitEthernet1/0/17",
    " description Cosmos FMS Server",
    " switchport mode trunk",
    " switchport trunk allowed vlan 10,20,30,40,50,60,100",
    "exit",

    "write memory"
]

# Type each line with a delay so the terminal doesn’t die from input diarrhea
for line in config_commands:
    pyautogui.typewrite(line, interval=0.1)
    print(f"{line}")
    pyautogui.press('enter')
    time.sleep(0.5)

print("Done. Your terminal has been violated successfully.")
