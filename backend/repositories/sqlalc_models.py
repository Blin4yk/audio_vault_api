from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
    hash_password: Mapped[str] = mapped_column()



class Audio(Base):
    __tablename__ = "audios"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    file_name: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column()