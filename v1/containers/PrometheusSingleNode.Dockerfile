FROM ubuntu:22.04

# vim/curl are just for debugging
RUN apt-get update && apt-get install -y \
    vim \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /tsdb
WORKDIR /tsdb
COPY ./data/prometheus-2.45.1.linux-amd64.tar.gz  .
RUN tar xzf /tsdb/prometheus-2.45.1.linux-amd64.tar.gz \
  && chmod -R o+w .

# run forever
CMD tail -f /dev/null
