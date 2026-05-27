import os
import secrets
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models.models import Referral, RewardSystem, User


FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
BASE_REF_URL = os.getenv("BASE_REF_URL", "http://localhost:8000/api/r")


def generate_referral_token() -> str:
    return secrets.token_urlsafe(12)


def build_referral_link(token: str) -> str:
    return f"{BASE_REF_URL}/{token}"


def create_referee(db: Session, name: str, email: str, position: str) -> dict:
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        if not existing_user.referral:
            referral_token = existing_user.referral_token
            referral_link = existing_user.referral_link
            referral = Referral(
                referrer_id=existing_user.id,
                referral_token=referral_token,
                referral_link=referral_link,
                user_count=0,
                timestamp=datetime.now(timezone.utc),
            )
            db.add(referral)
            db.commit()
            db.refresh(existing_user)

        return {
            "user_id": existing_user.id,
            "referral_token": existing_user.referral_token,
            "referral_link": existing_user.referral_link,
        }

    for _ in range(5):
        token = generate_referral_token()
        referral_link = build_referral_link(token)

        existing_token = db.query(User).filter(User.referral_token == token).first()
        if existing_token:
            continue

        new_user = User(
            name=name,
            email=email,
            position=position,
            referral_token=token,
            referral_link=referral_link,
            timestamp=datetime.now(timezone.utc),
        )

        db.add(new_user)
        db.flush()

        referral = Referral(
            referrer_id=new_user.id,
            referral_token=token,
            referral_link=referral_link,
            user_count=0,
            timestamp=datetime.now(timezone.utc),
        )
        db.add(referral)
        db.commit()
        db.refresh(new_user)

        return {
            "user_id": new_user.id,
            "referral_token": new_user.referral_token,
            "referral_link": new_user.referral_link,
        }

    raise ValueError("Unable to generate a unique referral token")


def track_referral(db: Session, referral_token: str, referred_user_id: int) -> None:
    referee = db.query(User).filter(User.referral_token == referral_token).first()
    if not referee:
        raise ValueError("Invalid referral token")

    referral = db.query(Referral).filter(Referral.referral_token == referral_token).first()
    if not referral:
        referral = Referral(
            referrer_id=referee.id,
            referral_token=referral_token,
            referral_link=referee.referral_link,
            user_count=0,
            timestamp=datetime.now(timezone.utc),
        )

    referral.user_count += 1
    db.add(referral)
    db.commit()


def award_points(db: Session, referee_id: int, referred_user_id: int, points: int = 10) -> None:
    referral = db.query(Referral).filter(Referral.referrer_id == referee_id).first()
    if not referral:
        raise ValueError("Referral not found for the given referee")

    reward = RewardSystem(
        user_id=referee_id,
        referral_id=referral.id,
        reward_points=points,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(reward)
    db.commit()
