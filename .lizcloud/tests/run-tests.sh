#!/bin/bash

set -e

# Add /.local to path
export PATH=$PATH:/.local/bin

echo "Installing required packages..."
pip3 install -q -U --prefer-binary --user -r requirements.txt

# Disable qDebug stuff that bloats test outputs
export QT_LOGGING_RULES="*.debug=false;*.warning=false"

py.test -v $@

