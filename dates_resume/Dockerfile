FROM rabbitmq-python-base:0.0.1

COPY dates_resume /
COPY common/middleware /middleware
COPY common/config_reader /config_reader
COPY common/communication /communication
COPY common/status_checker /status_checker

ENTRYPOINT ["/bin/sh"]
