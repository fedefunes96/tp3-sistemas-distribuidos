FROM rabbitmq-python-base:0.0.1

COPY map_worker /
COPY common/middleware /middleware
COPY common/redirector /redirector
COPY common/config_reader /config_reader
COPY common/communication /communication

ENTRYPOINT ["/bin/sh"]
