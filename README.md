# S-Case Requirements Annotation tool #

## About ##

S-Case Requirements Annotation tool is a tool for annotating software requirements. The tool is created
within the context ofthe EU-funded project [S-CASE][scase].

This tool is largely based on the [brat annotation tool][brat]

## Installation ##

The steps for installing scase_rat are:
* Download the repo contents and place them in a folder named scase_rat
* Install apache2 (sudo apt-get install apache2)
* Move scase_rat folder in the folder of apache (/var/www/html/)
* Navigate to /var/www/html/scase_rat
* Execute install.sh
* Enable cgi in apache (sudo a2enmod cgi)
* Navigate to localhost/scase_rat, login as 'admin' (password: 'pass') and change your password

## License ##

The tool is available under the permissive [MIT License][mit] as is brat (http://brat.nlplab.org)
but incorporates software using a variety of open-source licenses, for details please see see LICENSE.md.

[scase]:  http://www.scasefp7.eu/
[brat]:  http://brat.nlplab.org/
[mit]:  http://opensource.org/licenses/MIT
