FROM ubuntu:22.04

# vim/curl are just for debugging
RUN apt-get update && apt-get install -y \
    vim \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /tsdb
WORKDIR /tsdb
COPY ./assets/prometheus-2.45.1.linux-amd64.tar.gz  .
RUN tar xzf /tsdb/prometheus-2.45.1.linux-amd64.tar.gz
WORKDIR /tsdb/prometheus-2.45.1.linux-amd64
COPY ./assets/prometheus.yml /tsdb/prometheus-2.45.1.linux-amd64/

# Needed as a bind-mount
RUN mkdir data

# Debug: run forever
# CMD tail -f /dev/null

CMD /tsdb/prometheus-2.45.1.linux-amd64/prometheus --config.file=/tsdb/prometheus-2.45.1.linux-amd64/prometheus.yml
#CMD ./prometheus --config.file=prometheus.yml
