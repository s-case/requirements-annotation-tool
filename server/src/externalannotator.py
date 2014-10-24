
from __future__ import with_statement

from message import Messager
from annotation import open_textfile
from common import ProtocolError
from config import DATA_DIR
from document import real_directory
from annotation import JOINED_ANN_FILE_SUFF, TEXT_FILE_SUFFIX
from os.path import join as join_path
from os.path import isdir, isfile, exists, abspath
from os import access, W_OK, makedirs

def auto_annotate(collection, docid):
    return {}
