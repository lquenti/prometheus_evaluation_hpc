// Collect implements the prometheus.Collector interface.
func (n NodeCollector) Collect(ch chan<- prometheus.Metric) {
  [...]
	// BENCHMARK BEGIN
	N := 1000
	// record the time
	totalStart := time.Now()
	for i := 0; i < N; i++ {
		n.RealCollect(ch)
	}
	totalEnd := time.Now()
	fmt.Println("total time: ", totalEnd.Sub(totalStart)
    .Milliseconds())
	fmt.Println("average time: ", float64(totalEnd.Sub(totalStart)
    .Milliseconds())/float64(N))
}

func (n NodeCollector) RealCollect(ch chan<- prometheus.Metric) {
	wg := sync.WaitGroup{}
	wg.Add(len(n.Collectors))
	for name, c := range n.Collectors {
		go func(name string, c Collector) {
			execute(name, c, ch, n.logger)
			wg.Done()
		}(name, c)
	}
	wg.Wait()
}
