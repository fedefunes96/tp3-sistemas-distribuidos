FROM rabbitmq-python-base:0.0.1

RUN apt update
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

RUN apt update

RUN apt-get install -y docker-ce docker-ce-cli containerd.io

COPY node_watcher /
COPY common/middleware /middleware
COPY common/config_reader /config_reader
COPY common/communication /communication
COPY common/status_checker /status_checker
COPY common/synchronization /synchronization

ENTRYPOINT ["/bin/sh"]
