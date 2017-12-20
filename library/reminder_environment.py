#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib
import os.path
import json

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
      present will create the environment if not present
      absent will delete the environment if present
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
- name: Create an environment named "staging" in project "awesome"
  reminder_environment:
    addr: 127.0.0.1:8000
    state: present
    project_name: "awesome"
    name: "staging"

- name: Delete the environment "staging" in the project "awesome"
  reminder_environment:
    addr: 127.0.0.1:8000
    state: absent
    project_name: "awesome"
    name: "staging"
'''


class ReminderManager(object):
    headers = {"Content-Type": "application/json"}
    projects_path = "/projects/"
    environments_path = "/environments/"
    reminders_path = "/reminders/"
    stacks_path = "/stacks/"

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

    def _get_environment(self, Id):
        path = os.path.join(self.environments_path, str(Id))
        self.conn.request('GET', "%s/" % path, None, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def _post_environment(self, project, name):
        body = json.dumps({'project': project, 'name': name})
        self.conn.request('POST', self.environments_path, body, self.headers)
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

    def create_env(self, project_id, name):
        status, data = self._post_environment(project_id, name)
        if status == 201:
            return data
        raise Exception(data)

    def get_env(self, env_id):
        status, data = self._get_environment(env_id)
        if status == 200:
            return data
        raise Exception(data)

    def delete_env(self, env_id):
        raise Exception("UNIMPLEMENTED")


def find_environment(environments, name):
    for env in environments:
        if env['name'] == name:
            return env

def main():

    argument_spec = dict(
        addr=dict(required=True, type='str'),
        state=dict(required=True, type='str',
                   choices=['present', 'absent']),
        project_name=dict(required=True, type='str'),
        name=dict(required=False, type='str', default=None),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    addr = module.params.get('addr')
    state = module.params.get('state')
    project_name = module.params.get('project_name')
    name = module.params.get('name')
    changed = False

    reminder = ReminderManager(addr)

    project = reminder.get_project(project_name)
    if project is None:
        module.fail_json(msg="Failed to create environment %s" % err)
    env = find_environment(project['environments'], name)

    if state == 'present':
        if env is None:
            try:
                env = reminder.create_env(project['id'], name)
                changed = True
            except Exception as err:
                module.fail_json(msg="Failed to create environment", error=str(err))
        data = reminder.get_env(env['id'])
        module.exit_json(changed=changed, environment=data)
    if state == 'absent':
        if env is not None:
            try:
                # TODO: implement the delete in the class
                env = reminder.delete_env(project['id'], name)
                changed = True
            except Exception as err:
                module.fail_json(msg="Failed to delete environment", error=str(err))
        module.exit_json(changed=changed)

    module.fail_json(msg="unexpected failure")

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == "__main__":
    main()
