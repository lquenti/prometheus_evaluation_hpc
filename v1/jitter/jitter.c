#include<mpi.h>
#include<mpi_proto.h>
#include<stdio.h>
#include<stdlib.h>
#include<time.h>

// We expect 8 byte time_t (less is okay)
// Thus, in order to have 128MiB buffer
const size_t BUFFER_SIZE = 128*1024*1024 / 8;
const size_t NUMBER_OF_RUNS = 20;

void fill(time_t *buf, size_t len) {
  for (int i=0; i<len; ++i) {
    buf[i] = time(NULL);
  }
}

void save(time_t *buf, size_t buf_len, FILE *fp) {
  for (size_t i=0; i<buf_len; ++i) {
    fprintf(fp, "%lld\n", (long long)buf[i]);
  }
}

int main() {
  // init
  int rank, size;
  MPI_Init(NULL, NULL);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  // Allocate for each buffer, open timestamp
  time_t *buf = malloc(BUFFER_SIZE * sizeof(time_t));
  char filename[25];
  sprintf(filename, "output_size_%d_rank_%d.txt", size, rank);
  FILE *fp = fopen(filename, "w");
  MPI_Barrier(MPI_COMM_WORLD);

  for (size_t i=0; i<NUMBER_OF_RUNS; ++i) {
    fill(buf, BUFFER_SIZE);
    MPI_Barrier(MPI_COMM_WORLD);

    save(buf, BUFFER_SIZE, fp);
    MPI_Barrier(MPI_COMM_WORLD);
  }

  fclose(fp);
  MPI_Finalize();
  free(buf);
  return 0;
}

