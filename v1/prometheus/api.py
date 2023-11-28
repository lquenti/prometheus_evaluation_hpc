import os
import sys
import threading

from contextlib import asynccontextmanager
from fastapi import FastAPI, Response

counter = 0
counter_lock = threading.Lock()

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

    # TODO make dynamic
    metrics = [
        "some_key 1337",
        "another_key 42",
    ]

    metrics_data = "\n".join(metrics)
    response.headers["Content-Type"] = "text/plain; version=0.0.4"
    return Response(content=metrics_data, media_type="text/plain")
