from pydantic import (
    model_validator
)

from model.user_model import BaseUserModel
from model.constants import Gender
from utils.repairer_after import (
    auto_correct_gender
)

class UserModelPost(BaseUserModel):
    @model_validator(mode='before')
    @classmethod
    def validate_modal(cls, data):
        if isinstance(data, dict):
            if not Gender.has_value(data.get('gender')):
                data.update({'gender': auto_correct_gender(data)})
        return data