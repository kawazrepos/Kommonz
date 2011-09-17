#!/bin/sh
PLATFORM=`uname`
PYTHON_VERSION=2.7.2

if [ "$PLATFORM" = 'Linux' ]; then
    echo "Installing required packages..."
    yes | sudo apt-get install curl python-all-dev python3-all-dev 
    yes | sudo apt-get install libreadline6-dev libsqlite3-dev libgdbm-dev
    yes | sudo apt-get install libbz2-dev build-essential libxml2-dev libxslt1-dev
fi

echo "Installing pythonbrew..."
curl -kL http://xrl.us/pythonbrewinstall | bash
source $HOME/.pythonbrew/etc/bashrc

echo "Add following lines on your rc file and hit return."
echo
echo "  [[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc"
echo
read INPUT

echo "Installing Python $PYTHON_VERSION with --enable-unicode=ucs4 options"
pythonbrew install --no-test --force --configure="--enable-unicode=ucs4" $PYTHON_VERSION
pythonbrew switch $PYTHON_VERSION
pythonbrew venv init
