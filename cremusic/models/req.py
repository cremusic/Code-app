import pydantic
from pydantic.utils import to_lower_camel


class BaseRequestModel(pydantic.BaseModel):
    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class PaginationParams(BaseRequestModel):
    next_token: int = pydantic.Field(default=0, ge=0)
    limit: int = pydantic.Field(default=20, gt=0)


class VerifyCodeRequest(BaseRequestModel):
    book_code: str = pydantic.Field(
        ...,
        max_length=6,
        min_length=6,
        regex=r"^[0-9A-Z]{6}$",
    )
    book_id: int = pydantic.Field(..., gt=0)
    telephone: str = pydantic.Field(
        ..., max_length=10, min_length=5, regex=r"^[+0][0-9]{5,10}$"
    )
    name: str
    email: pydantic.EmailStr | None = pydantic.Field(None)


class BookCodeConfigReq(BaseRequestModel):
    required_unlock: bool | None = pydantic.Field(None)
    global_code: str | None = pydantic.Field(None)
    secret: str


class PaginationWithBookCode(PaginationParams):
    book_code: str | None = pydantic.Field(None)
