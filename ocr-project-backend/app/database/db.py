import asyncpg

# from psycopg2 import pool
from app.core.settings import settings

class Database:
    def __init__(self):
        self.user = settings.DB_USER
        self.password = settings.DB_PASS
        self.host = settings.DB_URL
        self.port = settings.DB_PORT
        self.database = settings.DATABASE
        self._cursor = None

        self._connection_pool = None
        self.con = None

    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=10,
                    command_timeout=60,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )

            except Exception as e:
                print(e)

    async def fetch_rows(self, query: str):
        if not self._connection_pool:
            await self.connect()
        else:
            self.con = await self._connection_pool.acquire()
            try:
                result = await self.con.execute(query)
                return result
            except Exception as e:
                print(e)
            finally:
                await self._connection_pool.release(self.con)

    async def close(self):
        if not self._connection_pool:
            try:
                await self._connection_pool.close()
            except Exception as e:
                logger.exception(e)

