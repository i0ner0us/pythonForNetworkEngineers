from netmiko import ConnectHandler
import re
import getpass

# Define variables to use
username = input("Enter Username for Remote Devices: ")
password = getpass.getpass()
secret = input("Enter the enable password: ")
last4 = "." + input("Enter the full mac address in all lower case letters (e.g. 1111.aaaa.bbbb.2c2c): ")
file = open('switches.txt') # create a file in the same directory called switches.txt

def main():
    # Connect to each switch and run show mac address-table | include 
    for line in file:
        cisco_switch = {
            'device_type': 'cisco_ios', ## use cisco_ios for Catalyst Devices
            'ip': line.strip(),
            'username': username,
            'password': password,
            'secret': secret,
        } 
        net_connect = ConnectHandler(**cisco_switch)

        # verify you are in enable mode
        if secret:
            net_connect.enable()
        else:
            print("No Enable Secret Entered")
        
        hostname = net_connect.find_prompt()[:-1]
        output = net_connect.send_command("show mac address-table address " + str(last4))
        print("\n+++++++++++++++ Searching " + str(hostname) + "+++++++++++++++\n")
        print(output)

main()

exit()
