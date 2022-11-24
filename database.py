from sqlalchemy.orm import sessionmaker, declarative_base

from sqlalchemy import create_engine

sqlalchemy_url = "sqlite:///./users.db"

engine = create_engine(sqlalchemy_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
