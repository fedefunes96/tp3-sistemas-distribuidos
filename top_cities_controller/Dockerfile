FROM rabbitmq-python-base:0.0.1

COPY top_cities_controller /
COPY common/middleware /middleware
COPY common/config_reader /config_reader
COPY common/communication /communication

ENTRYPOINT ["/bin/sh"]
