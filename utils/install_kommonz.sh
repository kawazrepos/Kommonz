#!/bin/sh

# Build python environment
/bin/sh ./build_python_env.sh

# Create virtualenv for Kommonz
source $HOME/.pythonbrew/etc/bashrc
pythonbrew switch 2.7.2
pythonbrew venv create Kommonz
pythonbrew venv use Kommonz

# Install required packages
cd ../
python setup.py develop

# Execute Syncdb
python src/Kommonz/manage.py syncdb

echo "Execute following commands"
echo
echo " - src/Kawaz/manage.py runserver 5000"
echo "   To start develop webserver as localhost:5000"
echo " - src/Kawaz/manage.py shell"
echo "   Enter interpreter shell of Kommonz"
echo
