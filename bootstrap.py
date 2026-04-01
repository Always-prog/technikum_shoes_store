import time

from sqlalchemy import text

from app import create_app
from app.extensions import db
from app.services import ensure_public_bucket

MAX_RETRIES = 20
RETRY_DELAY_SECONDS = 2

app = create_app()


def wait_for_database():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            db.session.execute(text("SELECT 1"))
            db.session.commit()
            print("Database connection is ready.")
            return
        except Exception as exc:  # noqa: BLE001
            db.session.rollback()
            print(f"Database is not ready (attempt {attempt}/{MAX_RETRIES}): {exc}")
            time.sleep(RETRY_DELAY_SECONDS)
    raise RuntimeError("Database did not become ready in time.")


def wait_for_minio():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            ensure_public_bucket()
            print("MinIO bucket is ready.")
            return
        except Exception as exc:  # noqa: BLE001
            print(f"MinIO is not ready (attempt {attempt}/{MAX_RETRIES}): {exc}")
            time.sleep(RETRY_DELAY_SECONDS)
    raise RuntimeError("MinIO did not become ready in time.")


if __name__ == "__main__":
    with app.app_context():
        wait_for_database()
        db.create_all()
        wait_for_minio()
        print("Bootstrap complete.")
