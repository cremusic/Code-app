import pydantic
from pydantic.utils import to_lower_camel


class BaseResponse(pydantic.BaseModel):
    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class CheckBookCodeResponse(BaseResponse):
    valid: bool


class Book(BaseResponse):
    id: int
    background_image_url: str
    background_color_code: int
    name: str
    type: str

    class Config:
        orm_mode = True


class PaginatedBooks(BaseResponse):
    next_token: int
    required_unlock: bool 
    data: list[Book]
