#define N 1000000
timestamp BIG_ARRAY[N];

int main() {
  MPI_INIT();
  for (int i=0; i<10; ++i) {
    for (int j=0; j<N; ++j) {
      BIG_ARRAY[j] = get_time_now();
    }
    save_big_array();
    MPI_BARRIER(); /* sync */
  }
}
