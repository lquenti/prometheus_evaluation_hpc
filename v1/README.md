# TSDB Evaluation

TODO write me

## Things to note into the report
- Thanos vs Cortex
  - why the core devs dont even want you to cluster
  - [How you scale through federation](https://logz.io/blog/prometheus-architecture-at-scale/)
  - [how to scale via federation and sharding](https://www.robustperception.io/scaling-and-federating-prometheus/)
- related work
  - <https://github.com/timescale/tsbs>
  - <https://github.com/VictoriaMetrics/prometheus-benchmark>
  - <https://valyala.medium.com/prometheus-vs-victoriametrics-benchmark-on-node-exporter-metrics-4ca29c75590f>
- multi step process stolen from tsbs
- we seralize using orjson, because it is well benchmarked and native

- related work prom benchmarking:
    - [PromCon 2018: Automated Prometheus Benchmarking](https://www.youtube.com/watch?v=9LuVvVddJjg)
    - [OVH benchmarking remote storage](https://blog.ovhcloud.com/benchmarking-prometheus-like-a-pro-with-k6/)
    - [Victoriametrics benchmarking prometheus](https://github.com/VictoriaMetrics/prometheus-benchmark)
