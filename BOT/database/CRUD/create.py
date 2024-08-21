from database.core import db
from database.models import User


async def create_user(username: str, email: str, full_name: str = None):
    async with db.Session() as session:
        new_user = User(username=username, email=email, full_name=full_name)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
