#!/bin/bash

PYTHON_FLAGS=$( python-config --cflags )
MY_FLAGS=-fPIC
CYTHON_FLAGS=-a # for annotated html file


# NumPy include path is determined my running numpy.get_include() in the python shell
INCLUDE=/usr/local/lib/python2.7/dist-packages/numpy/core/include

BASE=Base_2

rm ${BASE}*.{c,cpp,html,so}

cython ${CYTHON_FLAGS} ${BASE}.pyx
gcc ${PYTHON_FLAGS} ${MY_FLAGS} -I${INCLUDE} -shared ${BASE}.c -o ${BASE}.so

cython ${CYTHON_FLAGS} --cplus ${BASE}_cpp.pyx
g++ ${PYTHON_FLAGS} ${MY_FLAGS} -I${INCLUDE} -shared ${BASE}_cpp.cpp -o ${BASE}_cpp.so


