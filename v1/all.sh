echo "from all.sh"
echo $(pwd)
cd prometheus
./full_benchmark.sh
cd ..
#cd node_exporter
#./run_all_benchmarks.py