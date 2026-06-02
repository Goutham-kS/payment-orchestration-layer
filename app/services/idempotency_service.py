import hashlib

from sqlalchemy.orm import Session

from app.db.idempotency import IdempotencyKey


class IdempotencyService:

    @staticmethod
    def generate_request_hash(data: dict):

        return hashlib.sha256(
            str(data).encode()
        ).hexdigest()

    @staticmethod
    def get_key(
        db: Session,
        key: str
    ):

        return db.query(IdempotencyKey).filter(
            IdempotencyKey.key == key
        ).first()

    @staticmethod
    def create_key(
        db: Session,
        key: str,
        request_hash: str
    ):

        idem = IdempotencyKey(
            key=key,
            request_hash=request_hash,
            status="PROCESSING"
        )

        db.add(idem)

        db.commit()

        return idem

    @staticmethod
    def mark_completed(
        db: Session,
        key: str,
        response_body: dict,
        response_code: int = 200
    ):

        idem = db.query(IdempotencyKey).filter(
            IdempotencyKey.key == key
        ).first()

        idem.status = "COMPLETED"

        idem.response_body = response_body

        idem.response_code = response_code

        db.commit()

    @staticmethod
    def mark_failed(
        db: Session,
        key: str
    ):

        idem = db.query(IdempotencyKey).filter(
            IdempotencyKey.key == key
        ).first()

        if idem:

            idem.status = "FAILED"

            db.commit()