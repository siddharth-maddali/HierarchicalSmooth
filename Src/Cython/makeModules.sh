#!/bin/bash

PYTHON_FLAGS=$( python-config --cflags )
MY_FLAGS=-fPIC
CYTHON_FLAGS=-a # for annotated html file

cython ${CYTHON_FLAGS} Base_1.pyx
gcc ${PYTHON_FLAGS} ${MY_FLAGS} -shared Base_1.c -o Base_1_c.so

cython ${CYTHON_FLAGS} --cplus Base_1.pyx
g++ ${PYTHON_FLAGS} ${MY_FLAGS} Base_1.cpp -o Base_1_cpp.so


