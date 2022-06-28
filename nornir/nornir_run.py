from nornir import InitNornir
from nornir_csv.plugins.inventory import CsvInventory
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir_utils.plugins.functions import print_result


from datetime import date, datetime
import os

from nornir_netmiko import netmiko_send_command, netmiko_send_config

def task_apply_vlan_48(task):
    vlan_id = 48
    vlan_name = "nornir_test"

    config_cmds = [
    'vlan ' + str(vlan_id), 
    'name ' + str(vlan_name)]

    task.run(netmiko_send_config, config_commands=config_cmds)

def task_switch_vlan_based_on_mac(task):
    userMAC = "3b2d.1f"
    userVLAN = "48"

    showMAC = task.run(netmiko_send_command, command_string="show mac add | inc "+userMAC)

    print_result(showMAC)


def main():

    InventoryPluginRegister.register("CsvInventoryPlugin", CsvInventory)

    nr = InitNornir(config_file='sample_config.yaml')

    result = nr.run(task=task_switch_vlan_based_on_mac)

    print_result(result)


main()