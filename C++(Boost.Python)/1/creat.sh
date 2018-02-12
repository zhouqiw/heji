#!/bin/bash
echo "开始编译了"

student2py.o:student.o
g++ -c student2py.cpp -o student2py.o -fPIC -I/usr/include/python2.7 -I/home/mjf/lib/include

example.so:student.o student2py.o
    g++ student2py.o -o example.so -shared -fPIC -I/usr/include/python2.7 -I/home/mjf/lib/include -L/usr/lib/python2.7 -L/home/mjf/lib/lib -lboost_python
student.o:
    g++ -c student.cpp -o student.o

 
clean:
    rm -rf student.o student2py.o
    rm -rf example.so
python setup.py build_ext --inplace
