FROM frolvlad/alpine-glibc
#FROM ubuntu

MAINTAINER Michael Bartling "michael.bartling@arm.com"

# Install software 
RUN apk add --update \
    git \
    mercurial \
    python \
    perl \
    py-pip \
    build-base \
    python-dev \
    openssh-client \
    cmake

#RUN apt-get update
#RUN apt-get install -y \
#    git \
#    mercurial \
#    python \
#    python-pip \
#    python-dev \
#    openssh-client \
#    cmake

# Make ssh dir
RUN mkdir /root/.ssh/

# Copy over private key, and set permissions
ADD id_rsa /root/.ssh/id_rsa

# Create known_hosts
RUN touch /root/.ssh/known_hosts
# Add rsa key
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN pip install mbed-cli click

# Configure Git 
RUN git config --global url.ssh://git@github.com/.insteadOf https://github.com/
RUN git clone https://github.com/armmbed/mbed-cloud-client-example-restricted
WORKDIR /mbed-cloud-client-example-restricted

# Size Helping
RUN rm easy-connect.lib
RUN rm storage-selector.lib
RUN rm mbed-os.lib

RUN mbed config root .
RUN mbed deploy --protocol ssh

# Add developer certificate from user directory to project
ADD mbed_cloud_dev_credentials.c .
RUN pwd

#RUN python pal-platform/pal-platform.py -v deploy --target=x86_x64_NativeLinux_mbedtls generate
RUN python pal-platform/pal-platform.py fullbuild --target x86_x64_NativeLinux_mbedtls --toolchain GCC --external ./../define.txt --name mbedCloudClientExample.elf


# Run the linux client
CMD ["./out/Release/mbedCloudClientExample.elf"]
#ENTRYPOINT ["./out/Debug/mbedCloudClientExample.elf"]
