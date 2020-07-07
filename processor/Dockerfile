FROM rust:1.43

COPY processor .

RUN cargo build

ENTRYPOINT ["/bin/sh"]