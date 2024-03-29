from sqlalchemy import DateTime, func, BigInteger, String, ForeignKey

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)


class Location(Base):
    __tablename__ = 'location'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wedding_location: Mapped[str] = mapped_column(String(150), nullable=True)


class Cuisine(Base):
    __tablename__ = 'cuisine'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cuisine_type: Mapped[str] = mapped_column(String(150), nullable=True)


class Quiz(Base):
    __tablename__ = 'quiz'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    wedding_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    wedding_location_id: Mapped[int] = mapped_column(ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    cuisine_id: Mapped[int] = mapped_column(ForeignKey('cuisine.id', ondelete='CASCADE'), nullable=False)

    user: Mapped['User'] = relationship(backref='quiz')
    wedding_location: Mapped['Location'] = relationship(backref='quiz')
    cuisine: Mapped['Cuisine'] = relationship(backref='quiz')
