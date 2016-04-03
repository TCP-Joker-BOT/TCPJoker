#!/usr/bin/python3
import json
import logger
import os.path


def save_to_file(data):
    f = open('users.json', 'w')
    json.dump(data, f)
    f.close()


def register_user(username):
    global data
    data[username] = {'admin': False, 'groups': []}


def is_user_admin(username):
    global data
    return username in data and data[username]['admin']


def set_user_admin(username, admin_flag):
    global data
    if username not in data:
        register_user(username)
    data[username]['admin'] = admin_flag
    save_to_file(data)


def is_user_in_group(username, group):
    global data
    return username in data and group in data[username]['groups']


def add_user_to_group(username, group):
    global data
    if is_user_in_group(username, group):
        return
    data[username]['groups'].append(group)
    save_to_file(data)


def delete_user_from_group(username, group):
    global data
    if not is_user_in_group(username, group):
        return
    data[username]['groups'].remove(group)
    save_to_file(data)


try:
    data = json.load(open('users.json', 'r'))
    if type(data) != dict:
        raise ValueError
    else:
        for u in data['users'].values():
            if 'admin' not in u or type(u['admin']) != bool or 'groups' not in u or type(u['groups']) != list:
                raise ValueError
except FileNotFoundError:
    logger.info('File with users not found and will be created')
    data = {'users': {}}
except ValueError:
    logger.warning('Invalid users file, creating new')
    data = {'users': {}}
except:
    logger.warning('Some error occured with users file, creating new')
    data = {'users': {}}
