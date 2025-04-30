from domain.models.use_cases import GetUserByIdQuery
from infraestructure import UserFindSchema, UserRepository

from shared import exit_json
from shared.infraestructure.schemas import get_db

db = next(get_db())


class UserServiceImpl:
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
