#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = { 'metadata_version' : '1.0',
                     'status' : ['preview'],
                     'supported_by' : 'community'}


DOCUMENTATION = '''
---
module: cisco_ucs_sp_power
short_description: Power On/Off a server.
version_added: "2.3"
description:
    - Power on or off an ucs server.
options:
    state:
        description:
        - if C(up), will power on the server.
        - if C(down), will power off the server.
        required: true
        choices: ['up', 'down']
    chassis_id:
        description: ID of server's chassis.
        required: false
        default: None
    rack_id:
        description: ID of server's rack.
        required: false
        default: None
    blade_id:
        description: ID of server's blade (inside a chassis).
        required: false
        default: None

requirements: ['ucsmsdk', 'ucsm_apis']
author: Lucas Mattei(mattei.lucas@hotmail.com)
...
'''

EXAMPLES = '''
- name: Power on a blade on a chassis.
  cisco_ucs_power_set:
    state: "up"
    chassis_id: "2"
    blade_id: "3"
    ucs_ip: "192.168.242.140"
    ucs_username: "admin"
    ucs_password: "password"

- name: Power off a rack.
  cisco_ucs_power_set:
    state: "down"
    rack_id: "1"
    ucs_ip: "192.168.242.140"
    ucs_username: "admin"
    ucs_password: "password"
'''

def _argument_mo():
    return dict(
                chassis_id=dict(default=None, type='str'),
                rack_id=dict(default=None, type='str'),
                blade_id=dict(default=None, type='str')
    )

def _argument_connection():
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

def _argument_custom():
    return dict(
        state=dict(required=True,
                   choices=['up', 'down'],
                   type='str')
    )

def _ansible_module_create():
    argument_spec = dict()
    argument_spec.update(_argument_mo())
    argument_spec.update(_argument_custom())
    argument_spec.update(_argument_connection())

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)

def _get_mo_params(params):
    from ansible.module_utils.cisco_ucs import UcsConnection
    args = {}
    for key in _argument_mo():
        if params.get(key) is None:
            continue
        args[key] = params.get(key)
    return args


def set_power(server, module):
    from ucsmsdk.mometa.ls.LsPower import LsPower
    from ucsmsdk.mometa.ls.LsPower import LsPowerConsts
    from ucsm_apis.server.power import _server_dn_get
    from ucsmsdk.ucsexception import UcsOperationError


    ansible = module.params
    args_mo = _get_mo_params(ansible)

    dn = _server_dn_get(**args_mo)
    blade_mo = server.query_dn(dn)
    if blade_mo is None:
        raise UcsOperationError(
            "set_power: Failed to set server power",
            "server %s does not exist" % (dn))

    if blade_mo.assigned_to_dn is None:
        raise UcsOperationError(
            "set_power: Failed to set server power",
            "server %s is not associated to a service profile" % (dn))

    sp_mo = server.query_dn(blade_mo.assigned_to_dn)
    sp_pow = server.query_children(in_mo=sp_mo, class_id="LsPower")

    if ansible["state"] == "up":
        if sp_pow[0].state == LsPowerConsts.STATE_UP:
            return False
        LsPower(
            parent_mo_or_dn=sp_mo,
            state=LsPowerConsts.STATE_UP
        )

    else :
        if sp_pow[0].state == LsPowerConsts.STATE_DOWN:
            return False
        LsPower(
            parent_mo_or_dn=sp_mo,
            state=LsPowerConsts.STATE_DOWN
        )

    server.set_mo(sp_mo)
    server.commit()
    return True


def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = set_power(server,module)
    except Exception as e:
        err = True
        result["msg"] = "\n Setup error : %s \n" % str(e)
        result["changed"] = False

    return result, err

def main():
    from ansible.module_utils.cisco_ucs import UcsConnection

    module = _ansible_module_create()
    conn = UcsConnection(module)
    server = conn.login()

    result,err = setup(server,module)
    conn.logout()

    if err:
        module.fail_json(**result)
    module.exit_json(**result)

if __name__ == '__main__':
    main()
