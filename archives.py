# @router.get("/{user_id}")
# async def read_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
#     try:
#         cursor = db.cursor()
#         cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
#         user = cursor.fetchone()
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return {
#             "id": user[0],
#             "first_name": user[1],
#             "last_name": user[2],
#             "birthday": user[3],
#             "employee_number": user[4]
#         }
#     except sqlite3.Error as e:
#         logger.error(f"Error reading user: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# from fastapi import APIRouter, Depends, HTTPException, Request
# from pydantic import ValidationError
# from app.models import User
# import sqlite3
# from app.db import get_db
# import app.fdb as fast_db_functions 
# import logging # log msgs for debugging and error tracking

# # Set up basic logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# # create new router instance to define the routes related to user operations
# router = APIRouter()

# @router.post("/add_user")
# async def add_user(request: Request, db: sqlite3.Connection = Depends(get_db)):
#     try:
#         user_data = await request.json()
#         logger.debug(f"Received user data: {user_data}")
#         try:
#             user = User(**user_data) # validate and create a 'User' instance from the recieved data
#         # tldr: can't have leading zeros in json so this handles that
#         except ValidationError as e:
#             for error in e.errors():
#                 if error['loc'][0] == 'employee_number':
#                     raise HTTPException(
#                         status_code=422,
#                         detail="Employee number must not contain leading zeros. Please enter it without leading zeros."
#                     )
#             raise HTTPException(status_code=422, detail=str(e))
#         if user.employee_number is None:
#             try:
#                 user.employee_number = fast_db_functions.get_next_employee_number(db)
#             except sqlite3.Error as e:
#                 logger.error(f"Error getting next employee number: {e}")
#                 raise HTTPException(status_code=500, detail=str(e))
        
#         logger.debug(f"User data before inserting to DB: {user}")
#         try:
#             fast_db_functions.add_user_to_db(db, user.first_name, user.last_name, user.birthday, user.employee_number)
#             logger.debug("User added to DB successfully")
#             return {"message": "User added successfully"}
#         except sqlite3.Error as e:
#             logger.error(f"Error adding user to DB: {e}")
#             raise HTTPException(status_code=500, detail=str(e))
#     except Exception as e:
#         logger.error(f"Unexpected error: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.get("/get_users")
# async def get_users(db: sqlite3.Connection = Depends(get_db)):
#     try:
#         users = fast_db_functions.get_all_users(db)
#         for user in users:
#             user['employee_number'] = str(user['employee_number']).zfill(6)
#         return users
#     except sqlite3.Error as e:
#         logger.error(f"Error getting users: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
    
# @router.get("/{user_id}")
# async def read_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
#     try:
#         cursor = db.cursor()
#         cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
#         user = cursor.fetchone()
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return {
#             "id": user[0],
#             "first_name": user[1],
#             "last_name": user[2],
#             "birthday": user[3],
#             "employee_number": user[4]
#         }
#     except sqlite3.Error as e:
#         logger.error(f"Error reading user: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

