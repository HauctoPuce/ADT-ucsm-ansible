#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA={'metadata_version': '1.0',
                  'status': ['preview'],
                  'supported_by': ['community']}

DOCUMENTATION= '''
---
module: cisco_ucs_get_inventory
short_description: retrieve an UCS's inventory.
version_added: "2.3"
description:
    - retrieves an UCS's inventory in a json format
    - exports a table version of this inventory

options:
    display:
        description:
            - if C("yes") exports both a json and an ASCII Table version of the inventory.
            - if C("no") exports only a json version of the inventory
        required: false
        choices:['yes', 'no']
        default: 'no'

requirements: ['ucsmsdk', 'ucsm_apis', 'terminaltables']
author: Lucas Mattei (mattei.lucas@hotmail.com)

'''

EXAMPLES='''
- name : Retrieve inventory without display version.
  cisco_ucs_get_inventory:
    ucs_ip: "192.168.242.149"
    ucs_username: "admin"
    ucs_password: "password"
  register: result

- name: Retrieve inventory with display version.
  cisco_ucs_get_inventory:
    display: "yes"
    ucs_ip: "192.168.242.149"
    ucs_username: "admin"
    ucs_password: "password"
  register: result

- name: Print display version in a file.
  blockinfile:
    path: <YOUR/PATH>
    create: "yes"
    block: "{{result.display}}"

# see blockinfile.py module

'''

RETURN='''
inventory:
    description: json version of an inventory.
    returned: success
    type: string
    sample: {\"sys/chassis-5/blade-1\": {\"uuid\": \"1b4e28ba-2fa1-11d2-0501-b9a761bde3fb\",
            \"total_mem\": \"49152\", \"assigned_to_dn\": \"\", \"available_mem\": \"49152\",
             \"num_of_threads\": \"16\", \"oper_power\": \"off\", \"model\": \"UCSB-B200-M4\",
              \"serial\": \"SRV90\", \"association\": \"none\"}, ..., }

display:
    description: ASCII table version of an inventory.
    returned: success
    type: string
    sample:

+-----------------------+--------+----------------+--------------------------------------+------------+-------------+----------------+--------------------+-------+-----------------+---------+-------+
| Dn                    | Serial | Model          | UUID                                 | Associated | Assigned to | Total Mem (MB) | Available Mem (MB) | Disks | Total Disk Size | Threads | Power |
+-----------------------+--------+----------------+--------------------------------------+------------+-------------+----------------+--------------------+-------+-----------------+---------+-------+
| sys/chassis-5/blade-1 | SRV90  | UCSB-B200-M4   | 1b4e28ba-2fa1-11d2-0501-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 711 GB          | 16      | off   |
| sys/rack-unit-1       | RK39   | UCSC-C220-M4S  | 1b4e28ba-2fa1-11d2-e001-b9a761bde3fb | none       |             | 49152          | 49152              | 8     | 2 MB            | 16      | off   |
| sys/chassis-4/blade-2 | SRV89  | UCSC-C3K-M4SRB | 1b4e28ba-2fa1-11d2-0402-b9a761bde3fb | none       |             | 49152          | 49152              | 0     | 0 B             | 16      | off   |
| sys/rack-unit-5       | RK43   | UCSC-C220-M4L  | 1b4e28ba-2fa1-11d2-e005-b9a761bde3fb | none       |             | 49152          | 49152              | 8     | 43 MB           | 16      | off   |
| sys/chassis-3/blade-7 | SRV87  | UCSB-EX-M4-1   | 1b4e28ba-2fa1-11d2-0307-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 4 GB            | 32      | off   |
| sys/chassis-5/blade-3 | SRV92  | UCSB-B200-M4   | 1b4e28ba-2fa1-11d2-0503-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 711 GB          | 16      | off   |
| sys/chassis-5/blade-2 | SRV91  | UCSB-B200-M4   | 1b4e28ba-2fa1-11d2-0502-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 711 GB          | 16      | off   |
| sys/chassis-3/blade-3 | SRV85  | UCSB-EX-M4-1   | 1b4e28ba-2fa1-11d2-0303-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 838 KB          | 16      | off   |
| sys/chassis-4/blade-1 | SRV88  | UCSC-C3K-M4SRB | 1b4e28ba-2fa1-11d2-0401-b9a761bde3fb | none       |             | 49152          | 49152              | 0     | 0 B             | 16      | off   |
| sys/chassis-3/blade-1 | SRV84  | UCSB-EX-M4-1   | 1b4e28ba-2fa1-11d2-0301-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 838 KB          | 16      | off   |
| sys/rack-unit-3       | RK41   | UCSC-C220-M4S  | 1b4e28ba-2fa1-11d2-e003-b9a761bde3fb | none       |             | 49152          | 49152              | 8     | 2 MB            | 16      | off   |
| sys/rack-unit-2       | RK40   | UCSC-C240-M4S  | 1b4e28ba-2fa1-11d2-e002-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 931 KB          | 16      | off   |
| sys/chassis-5/blade-5 | SRV94  | UCSB-B420-M4   | 1b4e28ba-2fa1-11d2-0505-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 711 GB          | 32      | off   |
| sys/chassis-6/blade-1 | SRV95  | UCSC-C3K-M4SRB | 1b4e28ba-2fa1-11d2-0601-b9a761bde3fb | none       |             | 49152          | 49152              | 0     | 0 B             | 16      | off   |
| sys/rack-unit-6       | RK44   | UCSC-C460-M4   | 1b4e28ba-2fa1-11d2-e006-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 2 MB            | 32      | off   |
| sys/rack-unit-7       | RK45   | UCSC-C240-M4S  | 1b4e28ba-2fa1-11d2-e007-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 931 KB          | 16      | off   |
| sys/rack-unit-4       | RK42   | UCSC-C220-M4L  | 1b4e28ba-2fa1-11d2-e004-b9a761bde3fb | none       |             | 49152          | 49152              | 8     | 43 MB           | 16      | off   |
| sys/chassis-5/blade-4 | SRV93  | UCSB-B200-M4   | 1b4e28ba-2fa1-11d2-0504-b9a761bde3fb | none       |             | 49152          | 49152              | 2     | 711 GB          | 16      | off   |
+-----------------------+--------+----------------+--------------------------------------+------------+-------------+----------------+--------------------+-------+-----------------+---------+-------+

'''

### MODULE CLASS INSTANCIATION

def arg_custom():
    return dict(
        display=dict(
            default='no',
            choices=['yes','no'],
            type='str'
        )
    )

def arg_connection():
    return dict(
                ucs_server=dict(type='dict'),

                # Ucs server credentials
                ucs_ip=dict(type='str'),
                ucs_username=dict(default="admin", type='str'),
                ucs_password=dict(type='str', no_log=True),
                ucs_port=dict(default=None),
                ucs_secure=dict(default=None),
                ucs_proxy=dict(default=None)
    )

def _ansible_create_module():
    argument_spec = dict()
    argument_spec.update(arg_custom())
    argument_spec.update(arg_connection())
    return AnsibleModule(argument_spec=argument_spec,
                         supports_check_mode=True)

### MODULE'S CORE ALGORITHMS

def sizeof_fmt(size):
    fmt = [" B", " KB", " MB", " GB", " TB"]
    i = 0
    while size > 1024 and i < 4:
        size /= 1024
        i += 1
    return str(size) + fmt[i]


def get_diskInfo(handle, dnMO):
    nb_disk = 0
    total_size = 0

    dn = dnMO + "/board/storage-SAS-1"
    disks = handle.query_children(in_dn=dn, class_id="StorageLocalDisk")

    for disk in disks:
        if disk.size != "unknown":
            total_size += int(disk.size)
            nb_disk += 1

    return nb_disk, sizeof_fmt(total_size)


def get_infos(server, r):
    nb_disk, total_size = get_diskInfo(server,r.dn)

    return dict(
        assigned_to_dn= r.assigned_to_dn,
        association= r.association,
        oper_power= r.oper_power,
        model= r.model,
        serial= r.serial,
        total_mem = r.total_memory,
        num_of_threads = r.num_of_threads,
        available_mem = r.available_memory,
        uuid = r.uuid,
        nb_disk= nb_disk,
        total_size = total_size
    )

def print_inventory(inventory):
    from terminaltables import AsciiTable
    table_data = [
                ["Dn",
                 "Serial",
                 "Model",
                 "UUID",
                 "Associated",
                 "Assigned to",
                 "Total Mem (MB)",
                 "Available Mem (MB)",
                 "Disks",
                 "Total Disk Size",
                 "Threads",
                 "Power"]
            ]

    for item_key in inventory:
        item = inventory[item_key]
        item_row = [
            item_key,
            item["serial"],
            item["model"],
            item["uuid"],
            item["association"],
            item["assigned_to_dn"],
            item["total_mem"],
            item["available_mem"],
            item["nb_disk"],
            item["total_size"],
            item["num_of_threads"],
            item["oper_power"]
        ]
        table_data.append(item_row)

    table = AsciiTable(table_data)

    return table.table



def get_inventory(server,module):
    import json

    inventory = dict()
    disp = ""
    racks = server.query_classids('computeRackUnit', 'computeBlade')

    # Query infos about each rack.
    for id_key in racks:
        for r in racks[id_key]:
            inventory[r.dn] = get_infos(server, r)

    if module.params["display"] == "yes":
        disp = print_inventory(inventory)

    json_inventory = json.dumps(inventory)

    return json_inventory, disp





### MAIN

def setup(server, module):
    results = {}
    err = False

    try :
        results["inventory"], results["display"] = get_inventory(server, module)
    except Exception as e:
        err = True
        results["msg"]= "\n Setup Error: %s\n" % str(e)
    return results, err


def main():
    from ansible.module_utils.cisco_ucs import UcsConnection
    module = _ansible_create_module()
    conn = UcsConnection(module)
    server = conn.login()

    res, err = setup(server, module)

    conn.logout()
    if err:
        module.fail_json(**res)
    module.exit_json(**res)

if __name__ == '__main__':
    main()
