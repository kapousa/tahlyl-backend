import inspect
import json
from http.client import HTTPException
from sqlite3 import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from com.models.DigitalProfile import DigitalProfile as SQLDigitalProfile, DigitalProfile
from config import logger


def create_digital_profile(digital_profile: DigitalProfile, db: Session): # Ensure type hint is Pydantic DigitalProfile
    """
    Saves the new digital profile of the user and update previous saved digital profiles by setting recent = 0
    :param digital_profile: The Pydantic DigitalProfile object to save.
    :param db: The SQLAlchemy database session.
    :return: New Digital Profile (SQLAlchemy ORM object)
    """
    try:
        num_of_saved_profiles = db.query(SQLDigitalProfile).filter(
            SQLDigitalProfile.user_id == digital_profile.user_id, # Corrected: use dot notation
            SQLDigitalProfile.recent == 1
        ).count()

        if num_of_saved_profiles >= 1:
            db.query(SQLDigitalProfile).filter(SQLDigitalProfile.user_id == digital_profile.user_id).update(
                {"recent": 0},
                synchronize_session=False
            )
            db.commit()

        db_digital_profile = SQLDigitalProfile(
            id=digital_profile.id,
            user_id=digital_profile.user_id,
            health_overview=digital_profile.health_overview,
            recommendations=json.dumps(digital_profile.recommendations, ensure_ascii=False),
            attention_points=json.dumps(digital_profile.attention_points, ensure_ascii=False),
            risks=json.dumps(digital_profile.risks, ensure_ascii=False),
            creation_date=digital_profile.creation_date,
            recent= 1
        )
        db.add(db_digital_profile)
        db.commit()
        db.refresh(db_digital_profile)

        return db_digital_profile

    except Exception as e:
        func_name = inspect.currentframe().f_code.co_name
        logger.error(f"Error in '{func_name}': {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during saving the digital profile: {e}"
        )

