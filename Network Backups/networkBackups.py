from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException

ios_switches = open('iosSwitches.txt')
nxos_switches = open('nxosSwitches.txt')
ios_routers = open('iosRouters.txt')

def switchBackups():
    for line in ios_switches:
        cisco_switch = {
            'device_type': 'cisco_ios', ## use cisco_ios for Catalyst Devices
            'ip': line.strip(),
            'username': 'username',
            'password': 'password' ,
            'secret': 'secret',
        }

        ## Define Variables
        try:
            net_connect = ConnectHandler(**cisco_switch)
            hostname = net_connect.find_prompt()[:-1]

            ## Establish ssh connection and send backup commands
            net_connect.enable()
            net_connect.send_command('term len 0')
            output = net_connect.send_command('show run')

            ## Open file and write the running configs
            backup_file = open("./backups/" + str(hostname) + '.config', 'w')
            backup_file.write(output)
            backup_file.close()
            net_connect.disconnect()

            print("Backups of " + str(hostname) + " are complete and saved as " + str(hostname) + ".config\n")
        except (NetMikoTimeoutException, NetMikoAuthenticationException,) as error:
            print('Could not perform backup of ' + str(line) + '\nSee the following Error: \n' + str(error) + '\n')
            continue
        if not net_connect:
            net_connect.disconnect()

def nxosBackups():
    for line in nxos_switches:
        cisco_switch = {
            'device_type': 'cisco_nxos',
            'ip': line.strip(),
            'username': 'username',
            'password': 'password' ,
            'secret': 'secret',
        }

        ## Define Variables
        try:
            net_connect = ConnectHandler(**cisco_switch)
            hostname = net_connect.find_prompt()[:-1]

            ## Establish ssh connection and send backup commands
            net_connect.enable()
            net_connect.send_command('term len 0')
            output = net_connect.send_command('show run')

            ## Open file and write the running configs
            backup_file = open("./backups/" + str(hostname) + '.config', 'w')
            backup_file.write(output)
            backup_file.close()
            net_connect.disconnect()

            print("Backups of " + str(hostname) + " are complete and saved as " + str(hostname) + ".config\n")
        except (NetMikoTimeoutException, NetMikoAuthenticationException,) as error:
            print('Could not perform backup of ' + str(line) + '\nSee the following Error: \n' + str(error) + '\n')
            continue
        if not net_connect:
            net_connect.disconnect()

def routerBackups():
    for line in ios_routers:
        cisco_router = {
            'device_type': 'cisco_ios',
            'ip': line.strip(),
            'username': 'username',
            'password': 'password' ,
            'secret': 'secret',
        }

        ## Define Variables
        try:
            net_connect = ConnectHandler(**cisco_router)
            hostname = net_connect.find_prompt()[:-1]

            ## Establish ssh connection and send backup commands
            net_connect.enable()
            net_connect.send_command('term len 0')
            output = net_connect.send_command('show run')

            ## Open file and write the running configs
            backup_file = open("./backups/" + str(hostname) + '.config', 'w')
            backup_file.write(output)
            backup_file.close()
            net_connect.disconnect()

            print("Backups of " + str(hostname) + " are complete and saved as " + str(hostname) + ".config\n")
        except (NetMikoTimeoutException, NetMikoAuthenticationException,) as error:
            print('Could not perform backup of ' + str(line) + '\nSee the following Error: \n' + str(error) + '\n')
            continue
        if not net_connect:
            net_connect.disconnect()

print("+++++++++++++ Performing Cisco IOS Switch Backups +++++++++++++\n")
switchBackups()
print("+++++++++++++ Performing Cisco NX-OS Switch Backups +++++++++++++\n")
nxosBackups()
print("+++++++++++++ Performing Cisco Router Backups +++++++++++++\n")
routerBackups()

exit()
