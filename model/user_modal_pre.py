from pydantic import (
    field_validator
)

from model.user_model import BaseUserModel
from model.constants import Gender
from utils.repairer_before import (
    auto_correct_gender,
    auto_correct_mail
)

class UserModelPre(BaseUserModel):
    @field_validator('gender', mode='before')
    def validate_gender(cls, value):
        print('Go to validator gender: ', value)
        if Gender.has_value(value):
            return value
        return auto_correct_gender(value)
    
    @field_validator('email', mode='before')
    def validate_email(cls, value):
        print('Go to validator email: ', value)
        return auto_correct_mail(value)
    
    @field_validator('name', mode='before')
    def validate_name(cls, value):
        if value is None:
            raise Exception("The field name must not be empty!!!") 
        return value