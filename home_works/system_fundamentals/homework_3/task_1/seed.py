import getpass
import random

from faker import Faker
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.session import Session


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

class Status(Base):
    __tablename__ = "status"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

def get_psql_creds():
    username = input("Enter PSQL username (press enter for postgres): ")
    password = getpass.getpass("Enter PSQL password: ")
    host = input("Enter PSQL host (press enter for localhost): ")
    port = input("Enter PSQL port (press enter for 5432): ")

    username = username if username else "postgres"
    host = host if host else "localhost"
    port = port if port else "5432"

    return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/usersdb"

def get_db_engine():
    return create_engine(get_psql_creds())

def create_tables(engine):
    """Створює всі таблиці в базі даних"""
    Base.metadata.create_all(engine)

def fill_test_data(users_amount: int, tasks_per_user: int):
    fake = Faker(locale='uk_UA')
    statuses = ['new', 'in progress', 'completed']
    
    engine = get_db_engine()
    
    # Створюємо таблиці, якщо вони не існують
    create_tables(engine)
    
    # Спочатку створюємо базові статуси один раз
    with Session(engine) as session:
        for status_name in statuses:
            status = Status(name=status_name)
            session.add(status)
        session.commit()
    
    # Тепер заповнюємо користувачів і завдання
    with Session(engine) as session:
        # Отримуємо існуючі статуси
        status_objects = session.query(Status).all()
        
        for _ in range(users_amount):
            user = Users(fullname=fake.name(), email=fake.email())
            session.add(user)
            session.flush()  # Отримуємо ID користувача
            
            for _ in range(tasks_per_user):
                chosen_status = random.choice(status_objects)
                task = Tasks(
                    title=fake.sentence(),
                    description=fake.text(),
                    status_id=chosen_status.id,
                    user_id=user.id
                )
                session.add(task)
            
        session.commit()

if __name__ == "__main__":
    users_amount = int(input("Enter amount of users: "))
    tasks_per_user = int(input("Enter amount of tasks per user: "))
    fill_test_data(users_amount, tasks_per_user)