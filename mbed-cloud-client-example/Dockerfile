FROM ubuntu:14.04

MAINTAINER Michael Bartling "michael.bartling@arm.com"

RUN apt-get update
RUN apt-get install -y \
    rng-tools \
    git \
    mercurial \
    python \
    python-pip \
    perl \
    python-dev \
    build-essential \
    openssh-client \
    libpthread-stubs0-dev \
    cmake


# Install mbed tools
RUN pip install mbed-cli click requests

# Configure Git 
#RUN git config --global url.ssh://git@github.com/.insteadOf https://github.com/
RUN git clone https://github.com/armmbed/cola-tutorial.git
WORKDIR /cola-tutorial

# Size Helping as these are not used in Linux
RUN rm easy-connect.lib
RUN rm storage-selector.lib
RUN rm mbed-os.lib

RUN mbed config root .
RUN mbed deploy --protocol https

# Add developer certificate from user directory to project
ADD mbed_cloud_dev_credentials.c .
RUN pwd

# Use PAL tools to build Linux Client
RUN python pal-platform/pal-platform.py fullbuild --target x86_x64_NativeLinux_mbedtls --toolchain GCC --external ./../define.txt --name mbedCloudClientExample.elf


# Run the linux client
CMD ["./out/Release/mbedCloudClientExample.elf"]
#ENTRYPOINT ["./out/Debug/mbedCloudClientExample.elf"]
