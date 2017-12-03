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
  project_name:
    description:
      name of the project targeted by the operation
    required: true
  name:
    description: name of the targeted environent
    required: true
'''

EXAMPLES = '''
# Create a new project
reminder_environment:
  addr: 127.0.0.1:8000
  cmd: CREATE
  project_name: "awesome"
  name: "staging"
'''

import httplib
import os.path
import json
from pyreminder.base import ReminderManager

def find_environment(environments, name):
    for env in environments:
        if env['name'] == name:
            return env

def main():

    argument_spec = dict(
        addr=dict(required=True, type='str'),
        cmd=dict(required=True, type='str',
                 choices=['LIST', 'GET', 'CREATE', 'UPDATE', 'DELETE']),
        project_name=dict(required=True, type='str'),
        name=dict(required=False, type='str', default=None),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    addr = module.params.get('addr')
    cmd = module.params.get('cmd')
    project_name = module.params.get('project_name')
    name = module.params.get('name')
    changed = False

    reminder = ReminderManager(addr)

    project = reminder.get_project(project_name)
    env = find_environment(project['environments'], name)

    if cmd == 'CREATE':
       try:
           if env is None:
               data = reminder.create_env(project_id, name)
               changed = True
           else:
               data = reminder.get_env(env['id'])
       except Exception as err:
           module.fail_json(msg="Failed to create environment %s" % err)
    if cmd == 'GET':
        if env:
            data = reminder.get_env(env['id'])
        else:
            module.fail_json(msg="No environment named '%s' in project '%s'" % (name, project_name))
    if cmd == 'LIST':
        status, data = reminder.list_projects()

    module.exit_json(changed=changed, environment=data)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == "__main__":
    main()
