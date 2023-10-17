#!/bin/bash

python3.11 -m venv "env"
source env/bin/activate
pip install ../
pyinstaller ../server.spec
mkdir -p bin
cp dist/* bin/
deactivate
rm -rf env dist build
