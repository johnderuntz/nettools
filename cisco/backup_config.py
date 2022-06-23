# Author: John DeRuntz
# Purpose: Connects to a cisco IOS switch and backs up the config before editing the config.
# Credit: Inspired by some other authors found on Github
# https://github.com/AlexMunoz905/Python-Cisco-Backup/blob/master/ni_run_cisco.py
#
#
from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException
from paramiko.ssh_exception import SSHException 
from netmiko.ssh_exception import  AuthenticationException

from datetime import date, datetime
import os


def backup_cisco_config(host, username, password, enable_secret):
    # Set up folder and text file for backing up the config
    dt = datetime.now()
    dt_string = dt.strftime("%m-%d-%Y_%H-%M")
    # If the switch-config directory isnt made on the computer then create it
    if not os.path.exists('switch-config'):
        os.makedirs('switch-config')
    # Create the text file
    fileName = host + "_" + dt_string
    backupFile = open("switch-config/" + fileName + ".bkp", "w+")    

    # Create configuration for the SSH connection
    cisco_ios = {
    'device_type': 'cisco_ios',
    'host': host,
    'username': username,
    'password': password,
    'secret': enable_secret,
    }
    # Connect to the device
    try:
        print("Attempting connection to: " + host)
        net_connect = ConnectHandler(**cisco_ios)
    except (AuthenticationException):
        print ('Authentication Failure: ' + host)
    except (NetMikoTimeoutException):
        print ('\n' + 'Timeout to device: ' + host)
    except (SSHException):
        print ('SSH might not be enabled: ' + host)
    #If it connects successfully then send the enable privelaged commands
    net_connect.enable()
    print("Connection Successful!")
    # Get the config that is attached to the switch
    print("Executing 'show run' command...")
    config_output = net_connect.send_command("show run")
    # Save the config into a text file
    backupFile.write(config_output)
    print("Outputted to " + fileName + ".bkp!")    


     


