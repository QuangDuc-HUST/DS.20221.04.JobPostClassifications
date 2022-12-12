FROM apache/nifi:1.18.0
# LABEL maintainer="Faiez Zalila <faiez.zalila@cetic.be>"

USER root

# ENV SINGLE_USER_CREDENTIALS_USERNAME=admin 
# ENV SINGLE_USER_CREDENTIALS_PASSWORD=admin
RUN /bin/bash /opt/nifi/nifi-current/bin/nifi.sh set-single-user-credentials admin adminadminadmin

RUN apt-get update 
RUN apt install nano

# Install Python3
RUN apt-get install -y python3 python3-pip

# Install libraries 
# Note: the following list can be extended by libraries specific to your needs.

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install virtualenv
RUN virtualenv /opt/env
RUN . /opt/env/bin/activate && python3 -m pip install -r requirements.txt
COPY . .

WORKDIR /opt/nifi/nifi-current

RUN chmod -R 777 /code/scripts
# ENV PORT 8000
EXPOSE 8443


ENTRYPOINT ["../scripts/start.sh"]

# docker build -t project .
# docker run --name project -p 8443:8443/tcp -d project