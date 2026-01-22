import os

import asyncpg
from loguru import logger


def get_dsn_from_ssm(param_name: str) -> str:
    """Fetch DSN from AWS SSM Parameter Store."""
    import boto3
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return response["Parameter"]["Value"]


class Database:
    """Database operations for GTSF intake API."""

    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        env = os.environ.get("ENV", "local")
        
        if env == "production":
            logger.info("Production mode: fetching DSN from SSM...")
            dsn = get_dsn_from_ssm("/dsn/fishfact/service_gtsf_intake")
            logger.info("Connecting to PostgreSQL database...")
            self.pool = await asyncpg.create_pool(
                dsn=dsn,
                min_size=1,
                max_size=1,
            )
        else:
            logger.info("Local mode: connecting to local database...")
            self.pool = await asyncpg.create_pool(
                host="localhost",
                database="postgres",
                user="sam",
                min_size=1,
                max_size=1,
            )

    async def disconnect(self):
        if self.pool:
            logger.info("Closing database connection pool...")
            await self.pool.close()


# Singleton instance
db = Database()


async def get_conn():
    async with db.pool.acquire() as conn:
        yield conn