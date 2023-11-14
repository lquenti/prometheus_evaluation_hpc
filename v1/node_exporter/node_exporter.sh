NUMBER_OF_PROCESSES=1 # change me

./node_exporter --collector.disable-defaults \
  --collector.cpu \
  --collector.cpufreq \
  --collector.infiniband \
  --collector.meminfo \
  --collector.netdev \
  --collector.vmstat \
  --web.max-requests=0 \
  --runtime.gomaxprocs=${NUMBER_OF_PROCESSES}
