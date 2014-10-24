#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:

'''
Deletion functionality.
'''

from __future__ import with_statement

import os
from os.path import join as join_path
from message import Messager
from config import DATA_DIR
from session import get_session
from docimport import NoWritePermissionError, InvalidDirError
from document import real_directory
from os.path import isdir, isfile, abspath
from os import access, W_OK
from annotation import JOINED_ANN_FILE_SUFF, TEXT_FILE_SUFFIX

def delete_document(collection, document):
    #Messager.info(collection + ' ' + document)

    directory = collection

    if directory is None:
        dir_path = DATA_DIR
    else:
        #XXX: These "security" measures can surely be fooled
        if (directory.count('../') or directory == '..'):
            raise InvalidDirError(directory)

        dir_path = real_directory(directory)
    #Messager.info('dir_path: ' + dir_path)

    # Is the directory a directory and are we allowed to write?
    if not isdir(dir_path):
        raise InvalidDirError(dir_path)
    if not access(dir_path, W_OK):
        raise NoWritePermissionError(dir_path)

    ############################
    from session import get_session
    try:
        username = get_session()['user']
    except KeyError:
        username = None
    if username != 'admin':
        if (not username) or username + '/' not in dir_path:
            raise NoWritePermissionError(dir_path)
    ############################

    base_path = join_path(dir_path, document)
    txt_path = base_path + '.' + TEXT_FILE_SUFFIX
    ann_path = base_path + '.' + JOINED_ANN_FILE_SUFF
    #Messager.info('txt_path: ' + txt_path)
    #Messager.info('ann_path: ' + ann_path)

    if isdir(base_path):
        import shutil
        try:
            shutil.rmtree(base_path)
        except Exception as e:
            Messager.error(e, -1)

    # Delete the file
    for path in (txt_path, ann_path):
        #Messager.error("Removing " + path, -1)
        path = abspath(path)
        #Messager.error("Removing " + path, -1)
        if isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                Messager.error(e, -1)
                
            #Messager.info(path)

    #Messager.error("Document deletion not supported in this version.")
    Messager.info("Document removed!")
    return {}

def delete_collection(collection):
    Messager.error("Collection deletion not supported in this version.")
    return {}
     
