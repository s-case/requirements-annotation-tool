#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:

'''
Authentication and authorization mechanisms.

Author:     Pontus Stenetorp    <pontus is s u-tokyo ac jp>
            Illes Solt          <solt tmit bme hu>
Version:    2011-04-21
'''

from hashlib import sha512
from os.path import dirname, join as path_join, isdir, isfile
from os import listdir, makedirs

try:
    from os.path import relpath
except ImportError:
    # relpath new to python 2.6; use our implementation if not found
    from common import relpath
from common import ProtocolError
####################
from config import DATA_DIR
####################
from message import Messager
from session import get_session, invalidate_session
from projectconfig import ProjectConfiguration


# To raise if the authority to carry out an operation is lacking
class NotAuthorisedError(ProtocolError):
    def __init__(self, attempted_action):
        self.attempted_action = attempted_action

    def __str__(self):
        return 'Login required to perform "%s"' % self.attempted_action

    def json(self, json_dic):
        json_dic['exception'] = 'notAuthorised'
        return json_dic


# File/data access denial
class AccessDeniedError(ProtocolError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Access Denied'

    def json(self, json_dic):
        json_dic['exception'] = 'accessDenied'
        # TODO: Client should be responsible here
        Messager.error('Access Denied')
        return json_dic


class InvalidAuthError(ProtocolError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Incorrect login and/or password'

    def json(self, json_dic):
        json_dic['exception'] = 'invalidAuth'
        return json_dic


def _is_authenticated(user, password):
#     # TODO: Replace with a database back-end
#     ##############################
#     import json
#     with open('users.txt') as infile:
#         USER_PASSWORD = json.loads(infile.read())
#     ##############################
#     return (user in USER_PASSWORD and
#             password == USER_PASSWORD[user])
#             #password == _password_hash(USER_PASSWORD[user]))

    if isfile('users/' + user):
        with open('users/' + user) as infile:
            encrypter_password = infile.read()
        return encrypter_password == _password_hash(password)
    else:
        return False

def _password_hash(password):
    return sha512(password).hexdigest()

def login(user, password):
    if not _is_authenticated(user, password):
        raise InvalidAuthError

    get_session()['user'] = user
    Messager.info('Hello!')
    return {}

def register(user, password):
#     import json
#     with open('users.txt') as infile:
#         USER_PASSWORD = json.loads(infile.read())
#     if user in USER_PASSWORD:
#         Messager.info("Registration Failed! The username \"%s\" already exists!!" % user)
#     else:
#         USER_PASSWORD[user] = password
#         with open('users.txt', 'w') as outfile:
#             outfile.write(json.dumps(USER_PASSWORD))
#         ######################
#         if user != 'admin':
#             import os
#             mydatadir = path_join(DATA_DIR, user)
#             if not os.path.isdir(mydatadir):
#                 os.makedirs(mydatadir)
#                 myrobots = path_join(mydatadir, 'acl.conf')
#                 if not os.path.isfile(myrobots):
#                     with open(myrobots, 'w') as myrr:
#                         myrr.write("User-agent: " + user + "\nDisallow:\n\nUser-agent: admin\nDisallow:\n\nUser-agent: *\nDisallow:/\n")
#         ######################
#         Messager.info("Registration Complete! The username is \"%s\"" % user)
#     return {}

    usernames = listdir('users/')
    if user in usernames:
        Messager.info("Registration Failed! The username \"%s\" already exists!!" % user)
    else:
        with open('users/' + user, 'w') as outfile:
            outfile.write(_password_hash(password))
        if user != 'admin':
            mydatadir = path_join(DATA_DIR, user)
            if not isdir(mydatadir):
                makedirs(mydatadir)
                myrobots = path_join(mydatadir, 'acl.conf')
                if not isfile(myrobots):
                    with open(myrobots, 'w') as myrr:
                        myrr.write("User-agent: " + user + "\nDisallow:\n\nUser-agent: admin\nDisallow:\n\nUser-agent: *\nDisallow:/\n")
        Messager.info("Registration Complete! The username is \"%s\"" % user)
    return {}

def change_password(user, oldpassword, newpassword):
    if isfile('users/' + user):
        with open('users/' + user) as infile:
            encrypter_password = infile.read()
        if encrypter_password == _password_hash(oldpassword):
            with open('users/' + user, 'w') as outfile:
                outfile.write(_password_hash(newpassword))
            Messager.info("Password changed!")
        else:
            Messager.error('Wrong password!')
    else:
        Messager.error("You have to login first!")
    return {}

def logout():
    try:
        del get_session()['user']
    except KeyError:
        # Already deleted, let it slide
        pass
    # TODO: Really send this message?
    Messager.info('Bye!')
    return {}

def whoami():
    json_dic = {}
    try:
        json_dic['user'] = get_session().get('user')
    except KeyError:
        # TODO: Really send this message?
        Messager.error('Not logged in!', duration=3)
    return json_dic

def allowed_to_read(real_path):
    data_path = path_join('/', relpath(real_path, DATA_DIR))
    # add trailing slash to directories, required to comply to robots.txt
    if isdir(real_path):
        data_path = '%s/' % ( data_path )
        
    real_dir = dirname(real_path)
    robotparser = ProjectConfiguration(real_dir).get_access_control()
    if robotparser is None:
        return True # default allow

    try:
        user = get_session().get('user')
    except KeyError:
        user = None

    if user is None:
        user = 'guest'

    #display_message('Path: %s, dir: %s, user: %s, ' % (data_path, real_dir, user), type='error', duration=-1)

    return robotparser.can_fetch(user, data_path)

# TODO: Unittesting
