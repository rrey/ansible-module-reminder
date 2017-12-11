# -*- coding: utf-8 -*-

import httplib
import os.path
import json

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

    def _post_stack(self, reminder, name, hosts, urls):
        body = json.dumps({'reminder': reminder, 'name': name, 'hosts': hosts, 'urls': urls})
        self.conn.request('POST', self.stacks_path, body, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def _put_stack(self, Id, name, hosts, urls):
        path = os.path.join(self.stacks_path, str(Id))
        body = json.dumps({'name': name, 'hosts': hosts, 'urls': urls})
        self.conn.request('PUT', "%s/" % path, body, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def _get_reminder(self, Id):
        path = os.path.join(self.reminders_path, str(Id))
        self.conn.request('GET', "%s/" % path, None, self.headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def _get_stack(self, Id):
        path = os.path.join(self.stacks_path, str(Id))
        self.conn.request('GET', "%s/" % path, None, self.headers)
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

    def create_stack(self, reminder_id, name, hosts, urls):
        if hosts:
            hosts = [{'hostname': host} for host in hosts]
        if urls:
            urls = [{'url': url} for url in urls]
        status, data = self._post_stack(reminder_id, name, hosts, urls)
        if status == 201:
            return data
        raise Exception(data)

    def update_stack(self, stack_id, name, hosts, urls):
        if hosts:
            hosts = [{'hostname': host} for host in hosts]
        if urls:
            urls = [{'url': url} for url in urls]
        status, data = self._put_stack(stack_id, name, hosts, urls)
        if status == 200:
            return data
        raise Exception(data)

    def get_env(self, env_id):
        status, data = self._get_environment(env_id)
        if status == 200:
            return data
        raise Exception(data)

    def get_reminder(self, Id):
        status, data = self._get_reminder(Id)
        if status == 200:
            return data
        raise Exception(data)

    def get_stack(self, Id):
        status, data = self._get_stack(Id)
        if status == 200:
            return data
        raise Exception(data)
