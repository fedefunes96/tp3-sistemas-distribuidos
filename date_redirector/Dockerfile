FROM rabbitmq-python-base:0.0.1

COPY date_redirector /
COPY common/middleware /middleware
COPY common/redirector /redirector
COPY common/config_reader /config_reader
COPY common/communication /communication
COPY common/status_checker /status_checker

ENTRYPOINT ["/bin/sh"]
