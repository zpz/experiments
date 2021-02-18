ARG PARENT
FROM ${PARENT}
USER root

#------------------------------
# For writing Python extensions


RUN pip-install \
        'cython' \
        'cffi' \
        'numba' \
        'numpy' \
        'pybind11'

# `pybind11` header files are stored in /usr/local/include/python3.8m/pybind11/

RUN apt-update \
        apt-install gcc g++ libc-dev \
        apt-clean

# linker
RUN ln -s /usr/bin/gcc /usr/bin/cc

# A reasonable way to use clang-format (not installed):
#
# find ./ -iname *.h -o -iname *.cc -iname *.hpp -iname *.cpp \
#    | xargs \
#    clang-format -style="{BasedOnStyle: webkit, IndentWidth: 4, AccessModifierOffset: -2}" -i


#######################
### installing LLVM ###
#######################

# # Have had issues with installing LLVM.
# #
# # Refer to this page:
# #   https://apt.llvm.org
# #
# # This post may be informative:
# #  https://solarianprogrammer.com/2017/12/14/clang-in-docker-container-cpp-17-development/
# #
# # This page lists downloads, including prebuilt binaries (5.0.1 has debian; earlier versions do not):
# #  http://releases.llvm.org/download.html
# #
# # This page might be useful as well:
# #  https://llvm.org/docs/Docker.html
# 
# ENV LLVM_VERSION 5.0
# ENV LLVM_DESKTOP stretch
# 
# # This line used to be useful, but not any more.
# #RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv 15CF4D18AF4F7421 \
# 
# # `gnupg2` is needed to use `apt-key add -`.
# # `gnupg2` was removed in debian stretch.
# 
# RUN curl -skL --retry 3 http://apt.llvm.org/llvm-snapshot.gpg.key \
#         | apt-key add - \
#     && echo "deb http://apt.llvm.org/${LLVM_DESKTOP}/ llvm-toolchain-${LLVM_DESKTOP}-${LLVM_VERSION} main" > /etc/apt/sources.list.d/llvm.list \
#     && apt-get update \
#     && apt-get install -y --no-install-recommends \
#         libllvm${LLVM_VERSION} \
#         llvm-${LLVM_VERSION} \
#         llvm-${LLVM_VERSION}-dev \
#         clang-format-${LLVM_VERSION} \
#     && rm -rf /var/lib/apt/lists/* \
#     \
#     && ln -s /usr/bin/clang-format-${LLVM_VERSION} /usr/bin/clang-format \
#     && curl --retry 3 https://github.com/catchorg/Catch2/releases/download/v2.1.2/catch.hpp > /usr/local/include/catch.hpp \
#     && export LLVM_CONFIG=/usr/lib/llvm-${LLVM_VERSION}/bin/llvm-config

# Other packages often useful for software development:
#    autoconf=2.69-8 \
#    automake=1:1.14.1-4+deb8u1 \
#    binutils=2.25-5
#    libtool=2.4.2-1.11 \
#    zlib1g-dev=1:1.2.8.dfsg-2+b1 \
#
# `binutils` contains `gprof`.
# To use `gprof`, use option `-pg` during both compiling and linking.

# Rust

USER docker-user
RUN cd /tmp \
    && curl https://sh.rustup.rs -sSf > tt.sh \
    && sh tt.sh -y \
    && rm -rf tt.sh \
    && cd /home/docker-user/.cargo/bin \
    && ./rustup update nightly \
    && ./rustup default nightly
ENV PATH=/home/docker-user/.cargo/bin:$PATH
USER root


RUN pip-install \
        'setuptools-rust==0.10.6' 'pyo3-pack==0.4.2'

RUN pip-install faiss-cpu networkx
