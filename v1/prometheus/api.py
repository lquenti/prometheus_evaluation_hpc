from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/metrics")
def get_metrics(response: Response):
    # TODO make dynamic
    metrics = [
        "some_key 1337",
        "another_key 42",
    ]

    metrics_data = "\n".join(metrics)
    response.headers["Content-Type"] = "text/plain; version=0.0.4"
    return Response(content=metrics_data, media_type="text/plain")
