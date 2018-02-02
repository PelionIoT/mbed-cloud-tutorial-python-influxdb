FROM frolvlad/alpine-glibc

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

# HACKS because PAL depends on glibc magic
#RUN sed -i 's/enum __socket_type/unsigned int/' /mbed-cloud-client-example-internal/mbed-cloud-client/mbed-client-pal/Source/Port/Reference-Impl/OS_Specific/Linux/Networking/pal_plat_network.c
#RUN sed -i 's/sigval_t/union sigval/' /mbed-cloud-client-example-internal/mbed-cloud-client/mbed-client-pal/Source/Port/Reference-Impl/OS_Specific/Linux/RTOS/pal_plat_rtos.c
#RUN sed -i 's/__sched_priority/sched_priority/' /mbed-cloud-client-example-internal/mbed-cloud-client/mbed-client-pal/Source/Port/Reference-Impl/OS_Specific/Linux/RTOS/pal_plat_rtos.c

# Build The image
#RUN cd __x86_x64_NativeLinux_mbedtls \
#    && cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE=./../pal-platform/Toolchain/GCC/GCC.cmake -DEXTARNAL_DEFINE_FILE=./../define.txt \
#    && make mbedCloudClientExample.elf

# Run the linux client
CMD ["./out/Debug/mbedCloudClientExample.elf"]
