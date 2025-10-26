import logging
from sqlalchemy.orm import Session
from app.backend.core.database import SessionLocal
from app.backend.models.user import User
from app.data import seed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_db():
    db: Session = SessionLocal()
    try:
        if db.query(User).first():
            logger.info("Database already seeded. Skipping.")
            return
        logger.info("Seeding users...")
        demo_users = seed.get_demo_users()
        for user_data in demo_users:
            db_user = User(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                avatar_url=user_data["avatar"],
                city=user_data["city"],
                bio=f"Enjoys {', '.join(user_data['activities'])}.",
                verified_flag=user_data["verified_flag"],
            )
            db.add(db_user)
        db.commit()
        logger.info("Database seeded successfully with users!")
    except Exception as e:
        logger.exception(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Starting database seeding process...")
    seed_db()