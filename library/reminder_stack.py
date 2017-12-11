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
- name: Create a new stack inside a reminder
  reminder_stack:
    addr: 127.0.0.1:8000
    state: present
    reminder_id: 42
    name: "my stack name"

- name: Create a new stack with a list of hosts and urls
  reminder_stack:
    addr: 127.0.0.1:8000
    state: present
    reminder_id: 42
    name: "my stack name"
    hosts:
      - someserver-1.example.com
      - someserver-2.example.com
    urls:
      - http://someserver-1.example.com/admin
      - http://someserver-2.example.com/admin

- name: Delete a stack from a reminder
  reminder_stack:
    addr: 127.0.0.1:8000
    state: present
    reminder_id: 42
    name: "my stack name"
'''

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
        hosts=dict(required=False, type='list', default=[]),
        urls=dict(required=False, type='list', default=[]),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    addr = module.params.get('addr')
    state = module.params.get('state')
    reminder_id = module.params.get('reminder_id')
    name = module.params.get('name')
    hosts = module.params.get('hosts')
    urls = module.params.get('urls')

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
                stack = reminder.create_stack(my_reminder['id'], name, hosts, urls)
                changed = True
            except Exception as err:
                module.fail_json(msg="Failed to create stack %s" % err)
        data = reminder.get_stack(stack.get('id'))
        update = False
        current_hosts = [h['hostname'] for h in data['hosts']]
        # {{{ compare hosts and urls
        if hosts != current_hosts:
            update = True
        current_urls = [u['url'] for u in data['urls']]
        if urls != current_urls:
            update = True
        # }}}
        if update is True:
            try:
                stack = reminder.update_stack(my_reminder['id'], name, hosts, urls)
                changed = True
            except Exception as err:
                module.fail_json(msg="Failed to create stack %s" % err)
        data = reminder.get_stack(stack.get('id'))
        module.exit_json(changed=changed, stack=data)

    if state == 'absent':
        if stack is not None:
            try:
                # TODO: implement the delete in the class
                data = reminder.delete_stack(my_reminder.get('id'), name)
                changed = True
            except Exception as err:
                module.fail_json(msg="Failed to delete stack %s" % err)
        module.exit_json(changed=changed)

    module.json_fail(msg="unexpected failure")

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == "__main__":
    main()
