from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Database:
    def __init__(self, db_url: str = "sqlite:///db/documents.db"):
        self.engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()


class DocumentMetaData(Base):
    __tablename__ = "document_metadata"

    document_id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    chunking_strategy = Column(String, nullable=False)
    chunk_size = Column(Integer, nullable=False)
    total_chunks = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)



