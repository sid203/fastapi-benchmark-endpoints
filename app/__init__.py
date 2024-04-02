import time
import asyncio
from pydantic import BaseModel
from app.logging_utils import config_from_file, get_named_logger

config_from_file()
logger = get_named_logger(None)


class Payload(BaseModel):
    duration: int


def cpu_bound_workload(duration):
    logger.info(f"Triggering cpu bound workload, sleeping for {duration} seconds")
    time.sleep(duration)


async def io_bound_workload(duration):
    logger.info(f"Triggering IO bound workload sleeping for {duration} seconds")
    await asyncio.sleep(duration)