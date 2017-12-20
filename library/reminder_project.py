#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib
import os.path
import json

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

class ReminderManager(object):
    headers = {"Content-Type": "application/json"}
    projects_path = "/projects/"

    def __init__(self, addr):
        self.conn = httplib.HTTPConnection(addr)

    def _list_projects(self):
        self.conn.request('GET', self.projects_path, None, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def _get_project(self, name):
        path = os.path.join(self.projects_path, name)
        self.conn.request('GET', "%s/" % path, None, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def _post_project(self, name):
        body = json.dumps({'name': name})
        self.conn.request('POST', self.projects_path, body, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def get_project(self, name):
        status, data = self._get_project(name)
        if status == 200:
            return data

    def create_project(self, name):
        status, data = self._post_project(name)
        if status == 201:
            return data
        raise Exception(data)

    def delete_project(self, name):
        raise Exception("UNIMPLEMENTED")


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
