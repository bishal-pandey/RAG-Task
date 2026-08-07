from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class BookingDb:
    def __init__(self, db_url: str = "sqlite:///db/booking.db"):
        self.engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False} 
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


class BookingInfo(Base):
    __tablename__ = "booking_info"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String, primary_key=True, index=True)
    Email = Column(String, nullable=False)
    Date = Column(DateTime, nullable=False)
    Time = Column(DateTime, nullable = False)



