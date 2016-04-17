#!/usr/bin/python3
import json
import logger
import os.path


DATA_FILE_NAME = 'users.json'


def save_to_file(data):
    f = open(DATA_FILE_NAME, 'w')
    json.dump(data, f)
    f.close()


def is_user_registered(user_id):
    return str(user_id) in data


def register_user(user_id):
    global data
    data[str(user_id)] = {'admin': False, 'groups': []}


def is_user_admin(user_id):
    global data
    return str(user_id) in data and data[str(user_id)]['admin']


def set_user_admin(user_id, admin_flag):
    global data
    if str(user_id) not in data:
        register_user(str(user_id))
    data[str(user_id)]['admin'] = admin_flag
    save_to_file(data)


def is_user_in_group(user_id, group):
    global data
    return str(user_id) in data and group in data[str(user_id)]['groups']


def list_groups(user_id):
    global data
    if str(user_id) in data:
        return data[str(user_id)]['groups']
    else:
        return []


def add_user_to_group(user_id, group):
    global data
    if str(user_id) not in data:
        register_user(str(user_id))
    if is_user_in_group(str(user_id), group):
        return
    data[str(user_id)]['groups'].append(group)
    save_to_file(data)


def delete_user_from_group(user_id, group):
    global data
    if not is_user_in_group(str(user_id), group):
        return
    data[str(user_id)]['groups'].remove(group)
    save_to_file(data)


try:
    data = json.load(open(DATA_FILE_NAME, 'r'))
    if type(data) != dict:
        raise ValueError
    else:
        for u in data.values():
            if 'admin' not in u or type(u['admin']) != bool or 'groups' not in u or type(u['groups']) != list:
                raise ValueError
except FileNotFoundError:
    logger.info('File with users not found and will be created')
    data = {}
except ValueError:
    logger.warning('Invalid users file, creating new')
    data = {}
except:
    logger.warning('Some error occured with users file, creating new')
    data = {}
