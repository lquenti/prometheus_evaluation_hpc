CC = mpicc
CFLAGS = -Wall -Wextra

SRC = jitter.c
OUT = jitter_mpi

.PHONY: all clean

all: $(OUT)

# $@ == OUT, $< == SRC
$(OUT): $(SRC)
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(OUT)
