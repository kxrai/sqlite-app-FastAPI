from datetime import date, datetime
from pydantic import BaseModel, Field, validator, constr
import app.fdb as fdb 
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class User(BaseModel):
    first_name: str
    last_name: str
    birthday: str
    employee_number: int = Field(default=None, ge=1, le=999999)

    @validator('first_name')
    def validate_first_name(cls, value):
        if not value.isalpha():
            raise ValueError('Invalid characters')
        return value

    # @validator('birthday')
    # def validate_birthday(cls, value):
    #     logger.debug(f"Validating birthday in model: {value}")
    #     if not fdb.valid_birthday(value):
    #         logger.debug(f"Birthday validation failed for: {value}")
    #         raise ValueError('Invalid birthday')
    #     logger.debug(f"Birthday validation passed for: {value}")
    #     return value

    @validator('birthday')
    
    def validate_birthday(cls, value):
        print(f"Raw birthday value: {value}, type: {type(value)}")
        today = date.today()
        print(f"Today's date: {today}, type: {type(today)}")
        if isinstance(value, str):
            print("Parsing birthday from string")
            value = datetime.strptime(value, '%Y-%m-%d').date()
            print(f"Parsed birthday value: {value}, type: {type(value)}")
        if value > today:
            raise ValueError('Birthday cannot be in the future')
        if value.year < 1920:
            raise ValueError('Birthday cannot be before January 1, 1920')
        return value

    @validator('employee_number')
    def validate_employee_number(cls, value):
        if value is not None:
            if not (1 <= value <= 999999):
                raise ValueError("Employee number must be between 1 and 999999 and should not contain leading zeros. Please enter it without leading zeros.")
        return value
