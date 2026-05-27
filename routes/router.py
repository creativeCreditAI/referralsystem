import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.database import get_db
from models.models import Referral, RewardSystem, User
from models.schemas import SignupResponse, UserCreate
from services.referral import award_points, create_referee, track_referral
from services.email import send_welcome_email, send_referral_bonus_email

router = APIRouter()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


@router.post("/referral/", status_code=status.HTTP_201_CREATED, response_model=SignupResponse)
def create_referral(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_referee(db, payload.name, payload.email, payload.position)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/r/{token}", response_class=RedirectResponse)
def referral_redirect(token: str):
    frontend_signup = f"{FRONTEND_URL}/signup?ref={token}"
    return RedirectResponse(frontend_signup)


@router.post("/signup/", status_code=status.HTTP_201_CREATED, response_model=SignupResponse)
def signup(payload: UserCreate, ref: Optional[str] = Query(None), db: Session = Depends(get_db)):
    try:
        new_user = create_referee(db, payload.name, payload.email, payload.position)
        
        # Send welcome email to new user
        try:
            send_welcome_email(payload.email, payload.name, new_user["referral_token"])
        except Exception as e:
            print(f"Warning: Welcome email failed: {str(e)}")
        
        if ref:
            referrer = db.query(User).filter(User.referral_token == ref).first()
            if not referrer:
                raise ValueError("Invalid referral token")
            track_referral(db, ref, new_user["user_id"])
            award_points(db, referee_id=referrer.id, referred_user_id=new_user["user_id"])
            
            # Send reward email to the REFERRER (not the new user)
            try:
                send_referral_bonus_email(referrer.email, referrer.name, new_user["name"], reward_points=10)
            except Exception as e:
                print(f"Warning: Reward email failed: {str(e)}")
        
        return new_user
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/stats/")
def get_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_referrals = db.query(Referral).filter(Referral.user_count > 0).count()
    total_rewards = db.query(func.sum(RewardSystem.reward_points)).scalar() or 0

    return {
        "total_users": total_users,
        "total_referrals": total_referrals,
        "total_rewards": total_rewards,
    }
