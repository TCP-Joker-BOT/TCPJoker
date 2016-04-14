#!/usr/bin/python3
import users
import logger


def s_show_user_admin(user_id, _):
    if users.is_user_admin(user_id):
        return 'User {} is admin'.format(user_id)
    else:
        return 'User {} isn\'t admin'.format(user_id)


def s_set_user_admin(user_id, admin_flag):
    users.set_user_admin(user_id, admin_flag == 'true')
    return 'User {} admin status is now {}'.format(user_id, admin_flag)


def s_add_user_group(user_id, group_name):
    users.add_user_to_group(user_id, group_name)
    return 'User {} added to group {}'.format(user_id, group_name)


def s_delete_user_group(user_id, group_name):
    users.delete_user_from_group(user_id, group_name)
    return 'User {} deleted from group {}'.format(user_id, group_name)


def s_show_user_groups(user_id, _):
    user_groups = users.list_groups(user_id)
    return 'User {} is in following groups: {}'.format(user_id, ', '.join(user_groups))


def run(message):
    logger.info('Starting user control')
    if not users.is_user_admin(message['from']['id']):
        return 'Sorry, this option avaible only for admins'
    subcommands = {
        ('set', 'admin'): s_set_user_admin,
        ('show', 'admin'): s_show_user_admin,
        ('add', 'group'): s_add_user_group,
        ('delete', 'group'): s_delete_user_group,
        ('show', 'groups'): s_show_user_groups
    }
    msg = tuple(message['text'].split(' '))
    if len(msg) < 4:
        return 'Incorrect syntax, see /help for help'
    user_id = msg[1]
    logger.info('Operating with user {}'.format(user_id))
    command = msg[2:4]
    logger.info('Command: ' + ' '.join(command))
    tail = ' '.join(msg[4:])
    logger.info('Tail to pass: {}'.format(tail))
    if command in subcommands:
        return subcommands[command](user_id, tail)
    else:
        return 'Incorrect subcommand, see /help for help'
