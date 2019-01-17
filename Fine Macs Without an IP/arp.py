from netmiko import ConnectHandler
import sys
import getpass
import textfsm

def show_interface_switchport(ip, username, password, enable_secret):
    """
    get the access ports from the device using SSH

    :param ip: IP address of the device
    :param username: username used for the authentication
    :param password: password used for the authentication
    :param enable_secret: enable secret
    :return:
    """

    # establish a connection to the device
    ssh_connection = ConnectHandler(
        device_type='cisco_ios',
        ip=ip,
        username=username,
        password=password,
        secret=enable_secret
    )

    # enter enable mode
    ssh_connection.enable()

    # execute the show interface switchport to gather all interface modes
    results = ssh_connection.send_command("show interface switchport")

    # close SSH connection
    ssh_connection.disconnect()

    return results

def show_mac_address_table(ip, username, password, enable_secret, fsm_results):
    show_mac = ''
    mac_list = ''

    # establish a connection to the device
    ssh_connection = ConnectHandler(
        device_type='cisco_ios',
        ip=ip,
        username=username,
        password=password,
        secret=enable_secret
    )

    # enter enable mode
    ssh_connection.enable()

    # execute the show mac address table on every interface that is in static access mode
    for interface in fsm_results:
        if 'access' in interface[1]:
            show_mac += ssh_connection.send_command('show mac address-table interface ' + interface[0])

    ssh_connection.disconnect()

    # Run the text through the FSM.
    # The argument 'template' is a file handle and 'raw_text_data' is a
    # string with the content from the log.txt file
    template = open("template\cisco_ios_show_mac-address-table.textfsm")
    re_table = textfsm.TextFSM(template)
    mac_results = re_table.ParseText(show_mac)

    for mac in mac_results:
        mac_list += mac[1] + '\n'

    return mac_list

def show_ip_arp(ip, username, password, enable_secret, mac_list):
    # define variables to be used later
    arp_results = ''

    # establish a connection to the device
    ssh_connection = ConnectHandler(
        device_type='cisco_nxos',
        ip=ip,
        username=username,
        password=password,
        secret=enable_secret
    )

    # enter enable mode
    ssh_connection.enable()

    #send show ip arp command for every mac adress in mac_list
    for mac in mac_list:
        arp_results += ssh_connection.send_command("show ip arp | include " + str(mac))

    return arp_results

if __name__ == "__main__":
    '''
    get a list of all access port
    run show mac on every access port
    print the results
    '''

    # set variables
    ip = sys.argv[1]
    username = sys.argv[2]
    password = getpass.getpass()
    enable_secret = getpass.getpass()
    default_gateway = sys.argv[5]

    print('Gathering required data please wait... ')

    # get a list of access ports and store them as a variable
    all_switchports = show_interface_switchport(ip, username, password, enable_secret)

    # define the template to use to filter switchports
    template = open("template\cisco_ios_show-interface-switchport.textfsm")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(all_switchports)

    print('Almost Finished, thank you for your patience.... ')

    # get a list of all the mac address' and then gather an arp on every mac
    mac_list = show_mac_address_table(ip, username, password, enable_secret, fsm_results)

    print('Seriously, this script will be finished shortly!!!!')
    # get the arp response of every mac in the mac_list
    arp_results = show_ip_arp(default_gateway, username, password, enable_secret, mac_list.split('\n'))

    print('\n\nFINALLY!!!\n')

    invalid_arps = ''

    for mac in mac_list.split('\n'):
        if mac not in arp_results:
            invalid_arps += mac

    if invalid_arps:
        print('The following mac addresses do not show up in the arp table: \n\n' + str(invalid_arps) + '\n\n')
    else:
        print('The script ran successfully and did not find any issues!!\n\n')
