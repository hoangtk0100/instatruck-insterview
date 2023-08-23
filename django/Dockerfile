FROM python:3.9

# Setup code location
RUN mkdir /code
WORKDIR /code

# Install required packages
# Assume noninteractive mode, because running in Docker
ENV DEBIAN_FRONTEND noninteractive

# software-properties-common needed so we can add ppa's
#RUN apt-get update && apt-get install -y software-properties-common
# ubuntugis/ppa needed for gdal on Ubuntu
#RUN add-apt-repository ppa:ubuntugis/ppa

# note best practice: run as single command and remove apt directory at end
RUN apt-get update --quiet --yes && apt-get install --quiet --yes --no-install-recommends python3-pip
    # for cryptography build
#     build-essential libssl-dev libffi-dev python3-dev \
# #    ca-certificates \
#    python3-setuptools \
# #    python \
# #    libpq-dev \
#     gdal-bin && rm -rf /var/lib/apt/lists/*

# Cleanup
RUN apt-get clean

# Install required packages
ADD requirements.txt /code/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /code/requirements.txt

# Configure environment
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONWARNINGS d

# Entrypoint
# Also need
EXPOSE 8000-8100
WORKDIR /opt/project/

