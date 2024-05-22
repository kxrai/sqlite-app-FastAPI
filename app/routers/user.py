from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError
from app.models import User
import sqlite3
from app.db import get_db
import app.fdb as fast_db_functions 
import logging

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/add_user")
async def add_user(user: User, db: sqlite3.Connection = Depends(get_db)):
    try:
        logger.debug(f"Received user data: {user}")
        # If employee_number is not provided, assign a new one
        if user.employee_number is None:
            try:
                user.employee_number = fast_db_functions.get_next_employee_number(db)
            except sqlite3.Error as e:
                logger.error(f"Error getting next employee number: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        logger.debug(f"User data before inserting to DB: {user}")
        try:
            fast_db_functions.add_user_to_db(db, user.first_name, user.last_name, user.birthday, user.employee_number)
            logger.debug("User added to DB successfully")
            return {"message": "User added successfully"}
        except sqlite3.Error as e:
            logger.error(f"Error adding user to DB: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    except ValidationError as e:
        for error in e.errors():
            if error['loc'][0] == 'employee_number':
                raise HTTPException(
                    status_code=422,
                    detail="Employee number must not contain leading zeros. Please enter it without leading zeros."
                )
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_users")
async def get_users(db: sqlite3.Connection = Depends(get_db)):
    try:
        users = fast_db_functions.get_all_users(db)
        for user in users:
            user['employee_number'] = str(user['employee_number']).zfill(6)
        return users
    except sqlite3.Error as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail=str(e))
