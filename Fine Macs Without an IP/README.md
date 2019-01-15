# Finding Mac Addresses Without an IP on One switch
## Understanding the code
=====

#### Understanding the Syntax
=====
You can run the script [arp.py](./arp.py) with the following syntax

```
python3 ./arp.py [switch_ip] [auth_username] [auth_password] [auth_enable_secret] [default_gateway]
```

* Arguments:
..* switch_ip: should be replaced with the ip of the access switch which contains the mac list in question.
..* auth_username: should be replaced with a username who can authenticate against the switches.
..* auth_password: should be replaced with a password of the valid authenticated user.
..* auth_enable_secret: should be replaced with your enable password, even if it does not prompt for it.
..* default_gateway: should be replaced with the default_gateway where the arp_results exist.

#### Understanding the Code
======
##### Setting the Variables
------

```python
# set variables
ip = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
enable_secret = sys.argv[4]
default_gateway = sys.argv[5]
```

Using sys we define all variables needed to ssh into the switches to gather the data needed. With this we dont have files lying around with username and password written in clear text. Alternatively you can also define the information that is not so critical and us getpass() to get the password with a prompt. Also we can alternatively pass the others with raw input. See Below:

```python
import getpass
## using get pass
ip = input("Enter the IP of the Access Switch: ")
username = input("Enter the username you with to authenticate with: ")
password = getpass.getpass()
enable_secret = getpass.getpass()
default_gateway = input("Enter the IP of the default gateway: ")
```

##### Getting a list of interfaces to search through
------
Once we have the variables we need, it is time to do some research. the 'show_interface_switchport(ip, username, password, enable_secret)' function will go out to the access switch defined above, and get a list of every interface and the operational status using the command 'show interface switchport' on the switch.

After we have the list of interfaces we then parse through the list to store only active switchports in "static access" mode as a variable to reference later. We accomplish this with TextFSM with the following code using the [templates located in the template folder](./template/).

```python
# get a list of access ports and store them as a variable
all_switchports = show_interface_switchport(ip, username, password, enable_secret)

# define the template to use to filter switchports
template = open("template\cisco_ios_show-interface-switchport.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(all_switchports)
```

##### Getting a list of macs from the active switchports
------

Now we get the mac address from ever active interface stored in the all_switchports variable above:

```python
# get a list of all the mac address' and then gather an arp on every mac
mac_list = show_mac_address_table(ip, username, password, enable_secret, fsm_results)
```

After we have the mac addresses, we can then reach out the the default gateway and get the ip of each mac and store it again so that we can reference it later:

```python
# get the arp response of every mac in the mac_list
arp_results = show_ip_arp(default_gateway, username, password, enable_secret, mac_list.split('\n
```

#### Now we are talking
------

```python
invalid_arps = ''

for mac in mac_list.split('\n'):
    if mac not in arp_results:
        invalid_arps += mac

if invalid_arps:
    print('The following mac addresses do not have an ip address in the distribution switch:')
else:
    print('The script has completed successfully and found no issues.')
```
