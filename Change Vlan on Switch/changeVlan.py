from netmiko import ConnectHandler
import re
import sys

# Define username and password with prompt
# username = input("Enter Username for Remote Devices: ")
# password = getpass.getpass()
username = "username"
password = "password"
enable_secret = "enable secret"

if sys.argv:
    ip = str(sys.argv[1])
    switchport = str(sys.argv[2])
    vlan = str(sys.argv[3])
else:
    ip = input("\nEnter the ip of the switch you wish to configure: ")
    switchport = input("\nEnter the interface on which you wish to configure: ")
    vlan = input("\nEnter the vlan you wish to change the interface to: ")

# Define the device we want to check agains
cisco_switch = {
    'device_type': 'cisco_ios', ## use cisco_ios for Catalyst Devices
    'ip': ip,
    'username': password,
    'password': username,
    'secret': enable_secret,
} 

# Define Configs

config_commands = [
    'interface ' + str(switchport),
    'switchport access vlan ' + vlan]

# Set Variables to Connect to Swtich
net_connect = ConnectHandler(**cisco_switch)
hostname = net_connect.find_prompt()[:-1]

def main():
    output = net_connect.send_command("show int " + str(switchport) + " status")
    ifstatus = re.findall(r'connected', str(output), re.I|re.M)
    iftrunk = re.findall(r'trunk', str(output), re.I|re.M)
    output = net_connect.send_command("show vlan id " + vlan)
    ifvlan = re.findall(r'active', str(output), re.I|re.M)

    if len(ifstatus) > 0 and len(iftrunk) < 1 and len(ifvlan) > 0:
        print("All configs are good\n\n")
        print("+++++++++++++  Configuring Interface " + str(switchport) + "  +++++++++++++\n")
        config_interface = net_connect.send_config_set(config_commands)
        print(config_interface)
        exit()
    else:
        if len(ifstatus) < 1:
            print("\nInterface is not connected or disabled")
            output = net_connect.send_command("show int " + str(switchport) + " status")
            print(output + "\n\n")
        elif len(iftrunk) > 0:
            print("\nInterface is not an access port")
            output = net_connect.send_command("show int " + str(switchport) + " status")
            print(output + "\n\n")
        elif len(ifvlan) < 1:
            print("\nVlan does not exist or is not active")
            output = net_connect.send_command("show vlan id " + str(vlan))
            print(output + "\n\n")
        else:
            print("An Unknown error has occured. ")

# set if conditions (make sure port and vlan exist, and verify port is not a trunk)
if ip:
    show_version = net_connect.send_command("show ver")
    version = re.findall(r'IOS-XE', str(show_version))
    if len(version) > 0:
        net_connect.enable()
        main()
    else:
        main()        
else:
    print("No ip address was given, see documentation on proper usage:")
exit() 
