import pydantic


class ListBookPaginatorReq(pydantic.BaseModel):
    next_token: int = pydantic.Field(default=0, alias="nextToken", ge=0)
    limit: int = pydantic.Field(default=20, gt=0)


class VerifyCodeRequest(pydantic.BaseModel):
    # bookCode*	string pattern: ^[0-9A-Z]{6}$
    # bookId*	integer($int64)
    # telephone*	string pattern: ^[+0][0-9]{5,10}$
    # name*	string
    # email	string pattern: (^$)|(^(?=.{1,64}@)[A-Za-z0-9_-]+(\.[A-Za-z0-9_-]+)*@[^-][A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*(\.[A-Za-z]{2,})$)
    book_code: str = pydantic.Field(
        ...,
        alias="bookCode",
        max_length=6,
        min_length=6,
        regex=r"^[0-9A-Z]{6}$",
    )
    book_id: int = pydantic.Field(..., alias="bookId", gt=0)
    telephone: str = pydantic.Field(
        ..., max_length=10, min_length=5, regex=r"^[+0][0-9]{5,10}$"
    )
    name: str = pydantic.Field(...)
    email: pydantic.EmailStr | None = pydantic.Field(None)


class BookCodeConfigReq(pydantic.BaseModel):
    # requiredUnlock	boolean
    # globalCode	string
    # secret*	string
    required_unlock: bool | None = pydantic.Field(None, alias="requiredUnlock")
    global_code: str | None = pydantic.Field(None, alias="globalCode")
    secret: str = pydantic.Field(...)
