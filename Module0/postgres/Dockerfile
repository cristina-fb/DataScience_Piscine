FROM postgres:12-bullseye

COPY requirements.txt /home/
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install -r /home/requirements.txt