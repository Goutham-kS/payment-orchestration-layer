import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# =========================================================
# DATABASE URL
# =========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/payments_db"
)


# =========================================================
# DATABASE ENGINE
# =========================================================

engine = None

for i in range(30):

    try:

        engine = create_engine(
            DATABASE_URL
        )

        connection = engine.connect()

        connection.close()

        print("✅ Database connected")

        break

    except Exception:

        print(
            f"⏳ Waiting for DB... ({i+1}/30)"
        )

        time.sleep(2)


# =========================================================
# DATABASE FAILURE
# =========================================================

if engine is None:

    if os.getenv("PYTEST_RUNNING") != "1":

        raise Exception(
            "❌ Could not connect to database"
        )


# =========================================================
# SESSION
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# =========================================================
# BASE
# =========================================================

Base = declarative_base()


# =========================================================
# DB DEPENDENCY
# =========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================================================
# IMPORT ALL MODELS
# =========================================================

# IMPORTANT:
# Import ALL SQLAlchemy models here
# so Base.metadata.create_all() registers them.

from app.db.idempotency import IdempotencyKey

from app.db.models import (
    Transaction,
    ProcessedWebhookEvent
)