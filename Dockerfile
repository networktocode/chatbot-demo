FROM python:3.8-rc-slim-stretch

LABEL version="0.0.1"
LABEL description="ChatOps Demo"
LABEL maintainer="Rick Donato"

WORKDIR /workspace
COPY . /workspace

RUN apt-get update -y 
RUN apt-get install -y make vim tcpdump curl wget gcc procps net-tools ipcalc

RUN pip install -r requirements.txt 

CMD ["/bin/bash"]
