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

class ReminderManager(object):
    headers = {"Content-Type": "application/json"}
    projects_path = "/projects/"
    environments_path = "/environments/"

    def __init__(self, addr):
        self.conn = httplib.HTTPConnection(addr)

    def list_projects(self):
        self.conn.request('GET', self.projects_path, None, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def get_project(self, name):
        path = os.path.join(self.projects_path, name)
        self.conn.request('GET', "%s/" % path, None, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def post_project(self, name):
        body = json.dumps({'name': name})
        self.conn.request('POST', self.projects_path, body, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())


def main():

    argument_spec = dict(
        addr=dict(required=True, type='str'),
        cmd=dict(required=True, type='str',
                 choices=['LIST', 'GET', 'CREATE', 'UPDATE', 'DELETE']),
        project=dict(required=True, type='str'),
        environment=dict(required=False, type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    addr = module.params.get('addr')
    cmd = module.params.get('cmd')
    project = module.params.get('project')
    environment = module.params.get('environment')

    reminder = ReminderManager(addr)

    changed = False
    if cmd == 'CREATE':
        status, data = reminder.post_project(project)
        if status != 201:
            module.fail_json(msg="Command failed with status %d" % status,
                             data=data)
        changed = True
    if cmd == 'GET':
        status, data = reminder.get_project(project)
    if cmd == 'LIST':
        status, data = reminder.list_projects()

    module.exit_json(changed=changed, data=data, status=status)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == "__main__":
    main()
