from netmiko import ConnectHandler
import re
import getpass

# Define username and password
username = input('Enter Username for Remote Devices: ')
password = getpass.getpass()

# Define all the device we want to check agains
cisco_device1 = {
    'device_type': 'cisco_ios', ## use cisco_ios for Catalyst Devices and cisco_nxos for nexus devices
    'ip': '10.110.1.11',
    'username': username,
    'password': password,
} 

cisco_device2 = {
    'device_type': 'cisco_ios', ## use cisco_ios for Catalyst Devices and cisco_nxos for nexus devices
    'ip': '10.110.1.21',
    'username': username,
    'password': password,
} 

# Create a list of all devices for the following for loop
all_devices = [cisco_device1, cisco_device2]

for a_device in all_devices:
    
    # Establish Connection to the Device and define variables
    net_connect = ConnectHandler(**a_device)
    hostname = net_connect.find_prompt()[:-1]
    output = net_connect.send_command("show version")

    # Search the output for the version the switch is running and print it
    version = re.findall(r'Version\s16.[0-9][0-9].[0-9][0-9]', str(output), re.I|re.M)
    print("\n" + str(hostname) + " is running " + str(version))

exit() 
