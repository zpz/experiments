ARG PARENT
FROM ${PARENT}
USER root

#------------------------------
# For writing Python extensions

RUN apt-update \
        apt-install gcc g++ libc-dev \
        apt-clean


RUN pip-install \
        cython \
        cffi \
        numba \
        numpy \
        pybind11 \
	setuptools-rust

# `pybind11` header files are stored in /usr/local/include/python3.8m/pybind11/

# linker
#RUN ln -s /usr/bin/gcc /usr/bin/cc

#---------------------------------------
# Dependencies of specific code projects


RUN pip-install networkx

RUN pip-install zpz

