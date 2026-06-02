from sqlalchemy import Column, String, Integer, JSON, DateTime
from sqlalchemy.sql import func

from app.database import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    key = Column(String, primary_key=True, index=True)

    request_hash = Column(String, nullable=False)

    status = Column(String, nullable=False)

    response_code = Column(Integer)

    response_body = Column(JSON)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    expires_at = Column(DateTime(timezone=True))