# Contact email for users to use if the software encounters errors
ADMIN_CONTACT_EMAIL = CHANGE_ME

# Directories required by the brat server:
#
#     BASE_DIR: directory in which the server is installed
#     DATA_DIR: directory containing texts and annotations
#     WORK_DIR: directory that the server uses for temporary files
#
BASE_DIR = CHANGE_ME
DATA_DIR = CHANGE_ME
WORK_DIR = CHANGE_ME

# DEBUG
# Set to True to enable additional debug output

DEBUG = False


### LOG_LEVEL
# If you are a developer you may want to turn on extensive server
# logging by enabling LOG_LEVEL = LL_DEBUG

LL_DEBUG, LL_INFO, LL_WARNING, LL_ERROR, LL_CRITICAL = range(5)
LOG_LEVEL = LL_WARNING
#LOG_LEVEL = LL_DEBUG
