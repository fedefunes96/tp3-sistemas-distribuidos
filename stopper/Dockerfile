FROM rust:1.43

COPY stopper .

RUN cargo build

ENTRYPOINT ["/bin/sh"]