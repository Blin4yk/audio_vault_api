from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), unique=True, primary_key=True, index=True, default=uuid4
    )

class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()