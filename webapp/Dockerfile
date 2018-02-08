FROM python:jessie

MAINTAINER Michael Bartling "michael.bartling@arm.com"

# Install all system dependencies
RUN apt-get update
RUN apt-get install -y \
    git \
    gcc \
    python \
    python-pip \
    python-dev \
    openssh-client 


# Application lives here
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy our app from host machine to the Docker container
COPY . /usr/src/app

RUN pip install -r requirements.txt

ENV PYTHONPATH /usr/src/app
EXPOSE 8080

# Run the application
ENTRYPOINT ["python", "app.py"]
