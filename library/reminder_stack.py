#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: reminder
short_description: Handle communication with reminder-api.
description:
  - short_description: Handle communication with reminder-api.
options:
  addr:
    description: reminder api address
    required: true
  cmd:
    description:
      Operation to execute (CREATE, GET, LIST, DELETE)
    required: true
  project:
    description:
      name of the project targeted by the operation
    required: true
  environment:
    description: name of the project's environent targeted
    required: false
'''

EXAMPLES = '''
# Create a new project
reminder_project:
  addr: 127.0.0.1:8000
  cmd: CREATE
  project: "awesome"

# Get a project data
reminder_project:
  addr: 127.0.0.1:8000
  cmd: GET
  project: "awesome"
'''

import httplib
import os.path
import json
from pyreminder.base import ReminderManager


def find_stack(stacks, name):
    for stack in stacks:
        if stack['name'] == name:
            return stack

def main():

    argument_spec = dict(
        addr=dict(required=True, type='str'),
        cmd=dict(required=True, type='str',
                 choices=['LIST', 'GET', 'CREATE', 'UPDATE', 'DELETE']),
        reminder_id=dict(required=True, type='int'),
        name=dict(required=True, type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    addr = module.params.get('addr')
    cmd = module.params.get('cmd')
    reminder_id = module.params.get('reminder_id')
    name = module.params.get('name')
    changed = False

    reminder = ReminderManager(addr)
    r_data = reminder.get_reminder(reminder_id)

    if cmd == 'CREATE':
        stacks = r_data['stacks']
        s = find_stack(stacks, name)
        if not s:
            try:
                data = reminder.create_stack(r_data['id'], name)
                changed = True
            except Exception as err:
                module.fail_json(msg="Failed to create project %s" % err)
        else:
            data = reminder.get_stack(s['id'])

    if cmd == 'GET':
        data = reminder.get_stack(stack_id)
        if env_data is None:
            module.fail_json(msg="No environment named '%s' in project '%s'" % (environment, project))

    module.exit_json(changed=changed, stack=data)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == "__main__":
    main()
