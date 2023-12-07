import os
import random
import threading

from contextlib import asynccontextmanager
from fastapi import FastAPI, Response

# Change to configure
NUMBER_OF_METRICS=50
INT_RANGE = (0, 2**32)

counter = 0
counter_lock = threading.Lock()

# We do not want to rely on `random` for random numbers because it uses
# the current milliseconds as a seed. Since we are spawning that many processes
# parallely I would rather have a more independent seed.
#
# I thought about using `/dev/urandom` (through `os.urandom()`) but both the OS call
# and the byte-to-number-in-python conversion is too costly
#
# Thus, we do some middle-ground:
# - Get 8 random bits from os.urandom(), interpret as unsigned byte
# - Do that amount of warmup with mersenne random
# - use mersenne for following rng
warmup_iterations = int.from_bytes(os.urandom(1), byteorder='big')
rng = random.Random()
for _ in range(warmup_iterations):
    rng.random()

def inc():
    global counter
    global counter_lock
    with counter_lock:
        counter += 1

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # run first
    yield
    # save how many requests there were
    print("this happened")
    save_path = "./tmp_node_mock"
    if not os.path.exists(save_path):
        # maybe race condition, so okay if some other node exporter did it already
        os.makedirs(save_path, exist_ok=True)

    # We have the problem that we need a unique name
    # for each process for no race conditions between numbers
    # We use the pid.
    pid = os.getpid()
    save_file = f"{save_path}/reqs_{pid}.txt"
    assert not os.path.exists(save_file)

    with open(save_file, 'w') as fp:
        fp.write(str(counter))

app = FastAPI(lifespan=lifespan)

@app.get("/metrics")
def get_metrics(response: Response):
    inc()

    metrics = [
        f"keyname{i} {rng.randint(*INT_RANGE)}"
        for i in range(1, NUMBER_OF_METRICS+1)
    ]

    metrics_data = "\n".join(metrics)
    response.headers["Content-Type"] = "text/plain; version=0.0.4"
    return Response(content=metrics_data, media_type="text/plain")
