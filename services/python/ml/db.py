"""Postgres connection pool for ML training and inference code."""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg_pool import ConnectionPool


class DatabasePool:
    """Small adapter around psycopg_pool with a direct connection() smoke API."""

    def __init__(self, conninfo: str, max_size: int = 4) -> None:
        self._pool = ConnectionPool(
            conninfo=conninfo,
            min_size=0,
            max_size=max_size,
            open=False,
        )
        self._pool.open(wait=True)

    def connection(self) -> psycopg.Connection:
        return self._pool.getconn()

    def release(self, connection: psycopg.Connection) -> None:
        self._pool.putconn(connection)

    @contextmanager
    def borrow(self) -> Iterator[psycopg.Connection]:
        connection = self.connection()
        try:
            yield connection
        finally:
            self.release(connection)

    def close(self) -> None:
        self._pool.close()


def _database_url() -> str:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required for Python ML database access")
    return database_url


pool = DatabasePool(_database_url())
