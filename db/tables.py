from typing import List
from typing import Optional
from sqlalchemy import Text, DateTime, MetaData, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime


class Base(DeclarativeBase):
    metadata = MetaData(schema="mail_service")


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(Text())
    is_employee: Mapped[bool] = mapped_column(Boolean())
    name: Mapped[Optional[str]]
    chief_id: Mapped[Optional[int]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, chief_id={self.chief_id!r})"


class Mail(Base):
    __tablename__ = "mail"
    id: Mapped[int] = mapped_column(primary_key=True)
    from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    subject: Mapped[str] = mapped_column(Text())
    subject_type: Mapped[str] = mapped_column(Text())
    content: Mapped[str] = mapped_column(Text())

    from_: Mapped["User"] = relationship(foreign_keys=[from_id])
    to: Mapped["User"] = relationship(foreign_keys=[to_id])

    def __repr__(self) -> str:
        return f"Mail(id={self.id!r}, date={self.date!r}, " \
               f"subject={self.subject!r}, subject_type={self.subject_type!r}, content={self.content!r})"


