FROM rabbitmq-python-base:0.0.1

COPY map_worker /
COPY common/middleware /middleware
COPY common/redirector /redirector
COPY common/config_reader /config_reader
COPY common/communication /communication
COPY common/status_checker /status_checker
COPY common/secure_data /secure_data
COPY common/state_saver /state_saver
COPY common/coordinator /coordinator

ENTRYPOINT ["/bin/sh"]
