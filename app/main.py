import time
import asyncio
from app import Payload, cpu_bound_workload, io_bound_workload
from app.logging_utils import get_named_logger, config_from_file
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


config_from_file()
logger = get_named_logger(None)
process_pool = ProcessPoolExecutor(max_workers=8)

app = FastAPI(description="endpoints for testing sync/async workloads for concurrent requests")


@app.post("/test")
def test(payload: Payload):
    """
    Every request is handled in its own thread.
    """
    cpu_bound_workload(payload.duration)
    asyncio.run(io_bound_workload(payload.duration))
    return "OK"


@app.post("/test-async")
async def test_async(payload: Payload):
    cpu_bound_workload(payload.duration)
    await io_bound_workload(payload.duration)
    return "OK"


@app.post("/test-async2")
async def test_async_threadpool(payload: Payload):
    await run_in_threadpool(cpu_bound_workload, payload.duration)
    await io_bound_workload(payload.duration)
    return "OK"


@app.post("/test-async3")
async def test_async_threadpool3(payload: Payload):
    await run_in_threadpool(cpu_bound_workload, payload.duration)

    # does not work, coroutines are never awaited
    await run_in_threadpool(io_bound_workload, payload.duration)
    return "OK"


@app.post("/test-async4")
async def test_async_processpool(payload: Payload):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(process_pool, cpu_bound_workload, payload.duration)
    await io_bound_workload(payload.duration)
    return "OK"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", port=8000)
