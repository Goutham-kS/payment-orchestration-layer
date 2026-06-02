import asyncio

from app.database import SessionLocal

from app.db.models import Transaction

from app.services.reconciliation.engine import (
    ReconciliationEngine
)


class ReconciliationPoller:

    @staticmethod
    async def run():

        db = SessionLocal()

        try:

            transactions = db.query(
                Transaction
            ).all()

            results = []

            engine = ReconciliationEngine()

            for txn in transactions:

                result = await engine.reconcile_transaction(
                    db=db,
                    transaction=txn
                )

                results.append(result)

            return results

        finally:

            db.close()


# =====================================================
# OPTIONAL LOCAL TEST RUNNER
# =====================================================

if __name__ == "__main__":

    results = asyncio.run(
        ReconciliationPoller.run()
    )

    print(results)