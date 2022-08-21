from sqlmodel import create_engine, SQLModel, Session

sqlite_file_url = "sqlite:///database.db"

engine = create_engine(sqlite_file_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
