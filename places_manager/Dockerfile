FROM rabbitmq-python-base:0.0.1

COPY places_manager /
COPY common/middleware /middleware
COPY common/config_reader /config_reader
COPY common/communication /communication
COPY common/status_checker /status_checker
COPY common/secure_data /secure_data
COPY common/state_saver /state_saver

ENTRYPOINT ["/bin/sh"]
