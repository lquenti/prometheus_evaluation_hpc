# Results of Benchmarks done on [Emmy](https://gwdg.de/en/hpc/systems/emmy/)

Description of everything:
- `Untitled.ipynb` contains all analysis for reproducibility
- `prometheus_1node` contains the prometheus benchmarks using mock clients, running all mock nodes on a single node. 
  - This is relevant because, starting between 1500 and 2000 mock clients, the performance suffers HARD. Our working hypothesis is that this is because Linux cant handle that amount of open file descriptors, thus it should theoretically work when putting the mock clients onto multiple machines.
- `patched_node_exporter` is the e2e performance tests for the node exporter. See the report for a better description, but those benchmarks are valid.
- `node_exporter_faulty` were GREATLY designed benchmarks, unfortunately run against `node_exporter` `/`, which is a static HTML page, instead of `/metrics`, which actually in turn results in metric collection.
  - Thus it can be seen as some kind of baseline go net http performance, which is why we leave it in this repository
