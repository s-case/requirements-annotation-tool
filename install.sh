#!/bin/sh

# Install script for scase_rat
#
# Author:   Themistoklis Diamantopoulos
#

## Taken from install script for brat server
##
## Author:   Sampo Pyysalo       <smp is s u tokyo ac jp>
## Author:   Pontus Stenetorp    <pontus is s u tokyo ac jp>
## Version:  2012-02-09

# defaults

USERS_DIR=users
WORK_DIR=work
DATA_DIR=data
CONFIG_TEMPLATE=config_template.py
CONFIG=config.py

# Absolute data and work paths

base_dir=`(cd \`dirname $0\`; pwd)`
SCRIPT_NAME=`basename $0`

users_dir_abs="$base_dir/$USERS_DIR"
work_dir_abs="$base_dir/$WORK_DIR"
data_dir_abs="$base_dir/$DATA_DIR"

USAGE="Usage: ${SCRIPT_NAME} [-u]"

# Options
UNPRIVILEGED=false

while getopts u OPT; do
    case "${OPT}" in
        u)
            UNPRIVILEGED=true
            ;;
        \?)
            echo ${USAGE} 1>&2
            exit 1
            ;;
    esac
done
shift `expr $OPTIND - 1`

user_name=admin
password=pass
admin_email=admin@pass.com

# Put a configuration in place.

(echo "# This configuration was automatically generated by ${SCRIPT_NAME}"
cat "$base_dir/$CONFIG_TEMPLATE" | \
    awk 'NR==1 { print "from os.path import dirname, join as path_join" } $1' | \
    sed \
    -e 's|\(ADMIN_CONTACT_EMAIL = \).*|\1'\'$admin_email\''|' \
    -e "s|\(BASE_DIR = \).*|\1dirname(__file__)|" \
    -e "s|\(DATA_DIR = \).*|\1path_join(BASE_DIR, '${DATA_DIR}')|" \
    -e "s|\(WORK_DIR = \).*|\1path_join(BASE_DIR, '${WORK_DIR}')|") > "$base_dir/$CONFIG"

# Create directories

mkdir -p $work_dir_abs
mkdir -p $data_dir_abs

# Try to determine Apache group

apache_user=`ps aux | grep -v 'tomcat' | grep '[a]pache\|[h]ttpd' | cut -d ' ' -f 1 | grep -v '^root$' | head -n 1`
apache_group=`groups $apache_user | head -n 1 | sed 's/ .*//'`

# Make $work_dir_abs and $data_dir_abs writable by Apache

echo
echo "Setting global read and write permissions to directories"
echo "    \"$work_dir_abs/\" and"
echo "    \"$data_dir_abs/\" and"
echo "    \"$users_dir_abs/\""
echo "(you may wish to consider fixing this manually)"
chmod -R 777 $data_dir_abs $work_dir_abs $users_dir_abs

# Extract the most important library dependencies.

( cd server/lib && tar xfz simplejson-2.1.5.tar.gz )

# Dump some last instructions to the user
echo 'The installation has finished, you are almost done.'
echo
echo '1.) Add these lines to your apache2.conf file (/etc/apache2/apache2.conf)'
echo '    <Directory /var/www/html/scase_rat>'
echo '    AllowOverride Options Indexes FileInfo Limit'
echo '    AddType application/xhtml+xml .xhtml'
echo '    AddType font/ttf .ttf'
echo '    # For CGI support'
echo '    AddHandler cgi-script .cgi'
echo '    # Comment out the line above and uncomment the line below for FastCGI'
echo '    #AddHandler fastcgi-script fcgi'
echo '    </Directory>'
echo
echo '2.) Enable cgi in apache by executing'
echo '    sudo a2enmod cgi'
echo
echo '3.) Navigate to http://localhost/scase_rat, login as admin'
echo '    (password: pass) and change the admin password'
echo
