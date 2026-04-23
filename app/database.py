from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

# DATABASE_URL="postgresql://postgres:mypassword@localhost:5432/note-app"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mypassword@localhost:5432/note-app")

engine = create_engine(
    DATABASE_URL,
    echo=True
)

def get_session():
    with Session(engine) as session:
        yield session
        # FastAPI pattern

        # return session