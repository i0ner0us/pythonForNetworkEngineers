# pythonForNetworkEngineers
Python Scripts for Network Engineering (Mostly Cisco)

I have a few scripts that i have released publicly to share and collaborate on python best practices. A few scripts you can find assist in changing the vlan on a port while verifying that the port should be condifured as an accessport. Network backups is a neat script that will read a file for a list of ips to backup to a local directory called ./backups/{hostname}.config. There will be much more to come i am sure. 

# Installing Environment

All of my scripts are written in python version 3. 

1. Install Anaconda ( https://www.anaconda.com/download/)
2. From the Anaconda shell, run “conda install paramiko”
3. From the Anaconda shell, run “pip install scp”
4. Install git for windows (https://www.git-scm.com/downloads)
5. Clone Netmiko from Git Bash Window (https://github.com/ktbyers/netmiko)
6. Change directory to netmiko ("cd netmiko")
7. Run  python setup.py install from Git Bash Window ("python setup.py")
8. Check on Python console to confirm the availabilty of paramiko and netmiko libraryresult with following commands:
    a. python
    b. import paramiko
    c. import netmiko
    d. exit()

