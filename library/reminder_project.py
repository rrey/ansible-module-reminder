#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: reminder_project
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
  name:
    description:
      name of the project targeted by the operation
    required: true
'''

EXAMPLES = '''
- name: Create a project name "awesome"
  reminder_project:
    addr: 127.0.0.1:8000
    state: present
    project: "awesome"

- name: Delete the project named "awesome"
  reminder_project:
    addr: 127.0.0.1:8000
    state: absent
    project: "awesome"
'''

import httplib
import os.path
import json
from pyreminder.base import ReminderManager


def main():

    argument_spec = dict(
        addr=dict(required=True, type='str'),
        state=dict(required=True, type='str', choices=['present', 'absent']),
        name=dict(required=True, type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    addr = module.params.get('addr')
    state = module.params.get('state')
    name = module.params.get('name')
    changed = False

    reminder = ReminderManager(addr)
    data = reminder.get_project(name)

    if state == 'present':
        if data is None:
            try:
                data = reminder.create_project(name)
                changed = True
            except Exception as err:
                module.fail_json(msg="Failed to create project", error=str(err))
        module.exit_json(changed=changed, project=data)

    elif state == 'absent':
        if data is not None:
            try:
                # TODO: implement the delete in the class
                reminder.delete_project(name)
            except Exception as err:
                module.fail_json(msg="Failed to delete project", error=str(err))
        module.exit_json(changed=changed)

    module.fail_json(msg="unexpected failure")

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == "__main__":
    main()
