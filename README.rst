How to Install
============================
Enter the following commands on Terminal::

    cd ./utils
    sh ./install_kommonz.sh

The commands above will install python via pythonbrew and build virtualenv
for Kommonz.
After virtualenv has built, required python packages (listed below) will be installed.

Required python packages
----------------------------------
The list below may be expired. See ``install_requires`` values of ``setup.py``

-   setuptools
-   setuptools-git
-   dateutils
-   docutils
-   pyyaml
-   django>=1.3
-   django-compress
-   django-reversetag
-   django-pagination
-   django-mfw
-   django-qwert
-   django-object-permission

How to run
====================
Enter the following command on Terminal and visit http://localhost:5000/

    src/Kommonz/manage.py syncdb
    src/Kommonz/manage.py runserver 5000


