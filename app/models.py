from pydantic import BaseModel, Field, validator
import app.fdb as fdb 
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class User(BaseModel):
    first_name: str
    last_name: str
    birthday: str
    employee_number: int = Field(default=None, ge=1, le=999999)

    @validator('birthday')
    def validate_birthday(cls, value):
        logger.debug(f"Validating birthday in model: {value}")
        if not fdb.valid_birthday(value):
            logger.debug(f"Birthday validation failed for: {value}")
            raise ValueError('Invalid birthday')
        logger.debug(f"Birthday validation passed for: {value}")
        return value

    @validator('employee_number')
    def validate_employee_number(cls, value):
        if value is not None:
            if not (1 <= value <= 999999):
                raise ValueError("Employee number must be between 1 and 999999 and should not contain leading zeros. Please enter it without leading zeros.")
        return value
