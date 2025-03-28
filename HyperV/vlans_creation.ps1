# check if there is a virtual switch
# Create hyper v virtual switch if there isnt
New-VMSwitch -name vLanSwitch -NetAdapterName "Ethernet 6" -AllowManagementOs $true

# Check if the VLANs are already created
# if not, Create all the hyper v virtual network interfaces for the vlans