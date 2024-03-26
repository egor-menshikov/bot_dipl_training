from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Quiz, User


# Добавление опроса в базу
async def orm_add_quiz(session: AsyncSession, data: dict):
    obj = Quiz(
        user_id=data['user_id'],
        wedding_date=data['wedding_date'],
        wedding_location=data['wedding_location'],
        cuisine=data['cuisine'],
    )
    session.add(obj)
    await session.commit()


# Добавление юзера в базу
async def orm_add_user(
        session: AsyncSession,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id, first_name=first_name, last_name=last_name, phone=phone)
        )
        await session.commit()
