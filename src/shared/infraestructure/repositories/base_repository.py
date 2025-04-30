from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:

    def __init__(self, db_connection: AsyncSession):
        self.db_connection = db_connection
