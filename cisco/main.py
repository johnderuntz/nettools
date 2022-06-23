
from backup_config import *
import getpass





if __name__ == "__main__":

    ip = input("IP: ")
    username = input("Enter Useranme: ")
    password = getpass.getpass("Enter Password: ")
    secret = getpass.getpass("Enter Secret. If none hit enter: ")

    backup_cisco_config(ip, username, password, secret)
