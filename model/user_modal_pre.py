from pydantic import (
    field_validator
)

from model.user_model import BaseUserModel
from model.constants import Gender
from utils.repairer_before import (
    auto_correct_gender,
    auto_correct_mail
)

from prefect import task

class UserModelPre(BaseUserModel):
    @task
    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender(cls, value):
        print('Go to validator gender: ', value)
        if Gender.has_value(value):
            return value
        return auto_correct_gender(value)
    
    @task
    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, value):
        print('Go to validator email: ', value)
        if Gender.has_value(value):
            return value
        return auto_correct_mail(value)