FROM alpine:3.6

MAINTAINER Michael Bartling "michael.bartling@arm.com"

# Install software 
RUN apk add --update \
    git \
    gcc \
    build-base \
    python \
    py-pip \
    python-dev \
    libffi-dev \
    openssl-dev \
    openssh-client 

# Make ssh dir
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r requirements.txt

ENV PYTHONPATH /usr/src/app
EXPOSE 8080

# Run the linux client
ENTRYPOINT ["python", "app.py"]
