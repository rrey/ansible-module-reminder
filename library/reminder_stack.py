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
  state:
    description:
      present/absent
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
- name: Create new stack inside a reminder
  reminder_stack:
    addr: 127.0.0.1:8000
    state: present
    reminder_id: 42
    name: "my stack name"

- name: Delete a stack from a reminder
  reminder_stack:
    addr: 127.0.0.1:8000
    state: present
    reminder_id: 42
    name: "my stack name"
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
        state=dict(required=True, type='str', choices=['absent', 'present']),
        reminder_id=dict(required=True, type='int'),
        name=dict(required=True, type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    addr = module.params.get('addr')
    state = module.params.get('state')
    reminder_id = module.params.get('reminder_id')
    name = module.params.get('name')
    changed = False

    reminder = ReminderManager(addr)
    my_reminder = reminder.get_reminder(reminder_id)
    if not my_reminder:
        module.fail_json(msg="Reminder not found")
    stacks = my_reminder['stacks']
    stack = find_stack(stacks, name)

    if state == 'present':
        if stack is None:
            try:
                stack = reminder.create_stack(my_reminder['id'], name)
                changed = True
            except Exception as err:
                module.fail_json(msg="Failed to create stack %s" % err)
        data = reminder.get_stack(stack.get('id'))
        module.exit_json(changed=changed, stack=data)

    if state == 'absent':
        if stack is not None:
            try:
                # TODO: implement the delete in the class
                data = reminder.create_stack(my_reminder.get('id'), name)
                changed = True
            except Exception as err:
                module.fail_json(msg="Failed to delete stack %s" % err)
        module.exit_json(changed=changed)

    module.json_fail(msg="unexpected failure")

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == "__main__":
    main()
