"""
  Version: 0.0.1
  Progam name: LANdiscover
  Author: Jaryd Remillard
  Description:
    A simple script to get the DHCP leases and parse through the name, to spit out what hostnames are running on your LAN.
    This is used for my local lab so I can be even lazier by not remembering local hostnames. I can just refer to the output to remember what I named certain machines.
"""

import paramiko
import socket

# get dhcp leases from EdgeOS
# edgeos uses vyatta which uses vbash ¯\_(ツ)_/¯
# server is IP of the router, or if you can do local hostname resolution
# returns key/value pair as key is hostname and ip is value
def edgeos_get_dhcp_leases(server, username, password, output={}, hostname="vbash -c -i 'show dhcp leases' | awk -F' ' 'NR>2 {print $6}'", port=22):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, username=username, password=password)
        output = {}
        hostnames = []
        (stdin, stdout, stderr) = client.exec_command(ip)
        for line in stdout.readlines():
            if (line != "?\n"):
                hostnames.append(line.rstrip())
        client.close()
        for item in hostnames:
            output[item] = socket.gethostbyname(item)
        return output
    except Exception as e:
        print("Failed to connect to EdgeOS Router", e)