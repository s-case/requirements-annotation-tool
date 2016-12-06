# S-Case Requirements Annotation tool #

## About ##

S-Case Requirements Annotation tool is a tool for annotating software requirements. The tool is created
within the context of the EU-funded project [S-CASE][scase].

This tool is largely based on the [brat annotation tool][brat]

## Installation ##

The steps for installing scase_rat are:
* Download the repo contents and place them in a folder named scase_rat
* Install apache2 (sudo apt-get install apache2)
* Install python 2.7 and set it as default (sudo add-apt-repository ppa:fkrull/deadsnakes, sudo apt-get update, sudo apt-get install python2.7, sudo ln -s /usr/bin/python2.7 /usr/bin/python)
* Move the scase_rat folder in the folder of apache (/var/www/html/)
* Navigate to /var/www/html/scase_rat
* Execute install.sh
* Enable cgi in apache (sudo a2enmod cgi)
* If the previous step results in the message "Your MPM seems to be threaded. Selecting cgid instead of cgi.", then issue the commands sudo a2dismod mpm_event, sudo a2enmod mpm_prefork, sudo service apache2 restart, sudo a2enmod cgi, sudo service apache2 restart
* Make sure that the cgi files are executable (issue the command sudo chmod +x *.cgi)
* Navigate to localhost/scase_rat, login as 'admin' (password: 'pass') and change your password

## License ##

The tool is available under the permissive [MIT License][mit] as is the [brat annotation tool][brat]
but incorporates software using a variety of open-source licenses, for details please see see LICENSE.md.

[scase]:  http://www.scasefp7.eu/
[brat]:  http://brat.nlplab.org/
[mit]:  http://opensource.org/licenses/MIT
