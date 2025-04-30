from ...shared.application.helpers import exit_json
from ...shared.infraestructure.schemas.database import get_db

from ..domain.models.use_cases.queries.get_user_by_id import GetUserByIdQuery
from ..infraestructure.repositories.user_repository import UserRepository
from ..infraestructure.schemas.user_schema import UserFindSchema

db = next(get_db())


class UserServiceProvider:
    def __init__(self, db_session=db):
        self.user_repository = UserRepository(db_session)

    async def get_user_by_id(self, user_id: str):
        try:
            use_case = GetUserByIdQuery(self.user_repository)
            user = await use_case.execute(user_id)

            if user is None:
                return exit_json(0, {"message": "User not found"})

            user_map = UserFindSchema(
                id=user.id,
                name=user.name,
                email=user.email,
            )
            return exit_json(1, {"user": user_map})
        except Exception as e:
            return exit_json(0, {"message": str(e)})
