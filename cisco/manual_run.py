import getpass

from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException
from paramiko.ssh_exception import SSHException 
from netmiko.ssh_exception import  AuthenticationException

from datetime import date, datetime
import os




if __name__ == "__main__":

    # Get switch info
    host = input("IP: ")
    username = input("Enter Useranme: ")
    password = getpass.getpass("Enter Password: ")
    secret = getpass.getpass("Enter Secret. If none hit enter: ")

    # Create configuration for the SSH connection
    cisco_ios = {
    'device_type': 'cisco_ios',
    'host': host,
    'username': username,
    'password': password,
    'secret': secret,
    }


    exit = 0

    while exit == 0:
        print("-------------------------------")
        print("Please select an option:")
        print("1. Backup Config")
        print("2. Add new VLAN")
        print("3. Switch VLAN based on MAC address")
        print("4. Exit")
        print("-------------------------------")
        selection = input("Input: ")

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
        # If it connects successfully then send the enable privelaged commands
        net_connect.enable()
        print("Connection Successful!")
        #----------------------------------------------------#
        #                  BACKUP CONFIG                     #
        #----------------------------------------------------#
        if int(selection) == 1:
            print("Backing up Switch Configuration")
            # Set up folder and text file for backing up the config
            dt = datetime.now()
            dt_string = dt.strftime("%m-%d-%Y_%H-%M")
            # If the switch-config directory isnt made on the computer then create it
            if not os.path.exists('switch-config'):
                os.makedirs('switch-config')
            # Create the text file
            fileName = host + "_" + dt_string
            backupFile = open("switch-config/" + fileName + ".bkp", "w+")    
            print("Executing 'show run' command...")
            config_output = net_connect.send_command("show run")
            # Save the config into a text file
            backupFile.write(config_output)
            print("Outputted to " + fileName + ".bkp!")  
        #----------------------------------------------------#
        #                     ADD VLAN                       #
        #----------------------------------------------------#
        elif int(selection) == 2:
            # User input for VLANS
            vlan_id = input("Enter the VLAN ID you wish to add: ")
            vlan_name = input("Enter the VLAN Name: ")
            # Add the VLANS
            print("Adding VLAN " + vlan_id + " to " + host)
            config_cmds = [
                'vlan ' + str(vlan_id), 
                'name ' + str(vlan_name)]
            net_connect.send_config_set(config_cmds)
            print("VLAN Added")
        #----------------------------------------------------#
        #              SWITCH VLAN PER MAC                   #
        #----------------------------------------------------#
        elif int(selection) == 3:
            userMAC = input("\nVendor MAC for the devices. Must be HHHH.HH format: ")
            userVLAN = input("VLAN would you like the devices to be in: ")
            print("Searching for MAC addresses...")

            # run sh mac add | inc userMAC
            showMAC = net_connect.send_command("show mac add | inc "+userMAC)

            # grabs interfaces
            interfaces = [];
            for line in showMAC.splitlines():
                    #only grabs interfaces that are not equal to userVLAN
                    if line[2:4] != userVLAN:
                        interfaces.append(line[38:47].strip())

            print("\nFound these interfaces:")
            print(interfaces)

            # starts a loop to iterate
            for intf in interfaces:
                    output = net_connect.send_command("sh int "+intf+" status");

                    # skip if trunk
                    if "trunk" in output:
                        print("\n" +intf)
                        print("Skipping, port is a trunk.")

                    else:
                        print("\n" +intf)
                        print("Modifying, please wait...")

                        # issue commands
                        config_commands = [
                        'int '+intf,
                        'shut',
                        'swi acc vlan '+userVLAN,
                        'no shut']

                        net_connect.send_config_set(config_commands)
                        print("Done!")

            # write mem
            print("\nWriting to memory, please wait...")
            net_connect.send_command('write mem')

            
        #----------------------------------------------------#
        #                      EXIT                          #
        #----------------------------------------------------#
        elif int(selection) == 4:
            break
        #----------------------------------------------------#
        #                     EMPTY                          #
        #----------------------------------------------------#
        else:
            print("Invalid Input. Please Try Again")
