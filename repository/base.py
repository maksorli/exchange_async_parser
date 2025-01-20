from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

from repository.models import Base

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Логирование SQL-запросов
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Проверяем подключение

# with engine.connect() as connection:
#     result = connection.execute(text("SELECT current_database()"))


# Создаём таблицы

Base.metadata.create_all(bind=engine)
