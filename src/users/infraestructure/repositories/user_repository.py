from domain.repositories.user_repository_interface import \
    UserRepositoryInterface

from shared.infraestructure.database import user_table
from shared.infraestructure.repositories import BaseRepository


class UserRepository(BaseRepository, UserRepositoryInterface):
    def insert(self, report):
        with self.db_connection.begin():
            self.db_connection.execute(
                user_table.insert(),
                report.as_dict(),
            )
