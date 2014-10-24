#!/usr/bin/env python

from __future__ import with_statement

'''
Simple interface to for importing files into the data directory.

Author:     Pontus Stenetorp    <pontus is s u-tokyo ac jp>
Version:    2011-02-21
'''

from message import Messager
from annotation import open_textfile
from common import ProtocolError
from config import DATA_DIR
from document import real_directory
from annotation import JOINED_ANN_FILE_SUFF, TEXT_FILE_SUFFIX
from os.path import join as join_path
from os.path import isdir, isfile, exists, abspath
from os import access, W_OK, makedirs

### Constants
DEFAULT_IMPORT_DIR = 'import'
###


class InvalidDirError(ProtocolError):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return 'Invalid directory'

    def json(self, json_dic):
        json_dic['exception'] = 'invalidDirError'
        return json_dic


class FileExistsError(ProtocolError):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        apath = abspath(self.path)
        if apath.startswith('/brat/data'):
            apath = apath[len('/brat/data'):]
        return 'File exists: %s' % apath

    def json(self, json_dic):
        json_dic['exception'] = 'fileExistsError'
        return json_dic


class NoWritePermissionError(ProtocolError):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        apath = abspath(self.path)
        if apath.startswith('/brat/data'):
            apath = apath[len('/brat/data'):]
        return 'No write permission to %s' % apath

    def json(self, json_dic):
        json_dic['exception'] = 'noWritePermissionError'
        return json_dic


#TODO: Chop this function up
def save_import(text, docid, collection=None, anntext = None):
    '''
    TODO: DOC:
    '''
    
    if len(docid) > 4 and docid[-4] == '.':
        docid = docid[:-4]

    directory = collection

    if directory is None:
        dir_path = DATA_DIR
    else:
        #XXX: These "security" measures can surely be fooled
        if (directory.count('../') or directory == '..'):
            raise InvalidDirError(directory)

        dir_path = real_directory(directory)

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

    base_path = join_path(dir_path, docid)
    txt_path = base_path + '.' + TEXT_FILE_SUFFIX
    ann_path = base_path + '.' + JOINED_ANN_FILE_SUFF

    # Before we proceed, verify that we are not overwriting
    for path in (txt_path, ann_path):
        if isfile(path):
            raise FileExistsError(path)

    # Make sure we have a valid POSIX text file, i.e. that the
    # file ends in a newline.
    newtext = ''
    for line in text.splitlines():
        if line:
            newtext += line + '\n'
    text = newtext
    if text != "" and text[-1] != '\n':
        text = text + '\n'

    with open_textfile(txt_path, 'w') as txt_file:
        txt_file.write(text)

    if anntext:
        with open(ann_path, 'w') as ann_file:
            ann_file.write(anntext)
    else:
        # Touch the ann file so that we can edit the file later
        with open(ann_path, 'w') as _:
            pass

    return { 'document': docid }


def import_xmi(text, docid, collection=None):
    '''
    TODO: DOC:
    '''
    
    if len(docid) > 4 and docid[-4] == '.':
        docid = docid[:-4]

    directory = collection

    if directory is None:
        dir_path = DATA_DIR
    else:
        #XXX: These "security" measures can surely be fooled
        if (directory.count('../') or directory == '..'):
            raise InvalidDirError(directory)

        dir_path = real_directory(directory)

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

    base_path = join_path(dir_path, docid)
    xmi_path = base_path + '.zip'

    def decode_base64(data):
        import base64
        missing_padding = 4 - len(data) % 4
        if missing_padding:
            data += b'='* missing_padding
        return base64.decodestring(data)

    text = decode_base64(text[len("data:application/zip;base64,"):])
    #text = text.decode('base64')
    with open(xmi_path, 'wb') as thefile:
        thefile.write(text)
    #with open_textfile(xmi_path, 'wb') as xmi_file:
    #    xmi_file.write(text)

    return {}


def folder_import(docid, collection=None):
    '''
    TODO: DOC:
    '''

    directory = collection

    if directory is None:
        dir_path = DATA_DIR
    else:
        #XXX: These "security" measures can surely be fooled
        if (directory.count('../') or directory == '..'):
            raise InvalidDirError(directory)

        dir_path = real_directory(directory)

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

    base_path = join_path(dir_path, docid)
    base_path = abspath(base_path)

    # Before we proceed, verify that we are not overwriting
    if exists(base_path):
        raise FileExistsError(base_path)

    makedirs(base_path)

    return { 'document': base_path[len('/brat/data/'):] }

if __name__ == '__main__':
    # TODO: Update these to conform with the new API
    '''
    from unittest import TestCase
    from tempfile import mkdtemp
    from shutil import rmtree
    from os import mkdir


    class SaveImportTest(TestCase):
        test_text = 'This is not a drill, this is a drill *BRRR!*'
        test_dir = 'test'
        test_filename = 'test'

        def setUp(self):
            self.tmpdir = mkdtemp()
            mkdir(join_path(self.tmpdir, SaveImportTest.test_dir))
            mkdir(join_path(self.tmpdir, DEFAULT_IMPORT_DIR))

        def tearDown(self):
            rmtree(self.tmpdir)

        def test_import(self):
            save_import(SaveImportTest.test_text, SaveImportTest.test_filename,
                    relative_dir=SaveImportTest.test_dir,
                    directory=self.tmpdir)
        
        def test_default_import_dir(self):
            save_import(SaveImportTest.test_text, SaveImportTest.test_filename,
                    directory=self.tmpdir)
   

    import unittest
    unittest.main()
    '''
