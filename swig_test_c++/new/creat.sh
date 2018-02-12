#!/bin/bash
echo "Hello World !"

swig -python example.i
echo "swig is ok "
sudo python setup.py install
echo "install is ok"


