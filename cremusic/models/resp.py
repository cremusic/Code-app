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


class Episode(BaseResponse):
    # id	integer($int64)
    # bookId	integer($int64)
    # name	string
    # author	string
    # artist	string
    # backgroundImageUrl	string
    # backgroundColorCode	integer($int32)
    # unlocked	boolean
    # totalVideos	integer($int32)

    id: int
    book_id: int
    name: str | None
    author: str | None
    artist: str | None
    background_image_url: str | None
    background_color_code: int | None
    unlocked: bool
    total_videos: int

    class Config:
        orm_mode = True


class PaginatedEpisodes(BaseResponse):
    next_token: int
    data: list[Episode]


class NotFountResponse(BaseResponse):
    error: str = "not_found"
    message: str


class ServerErrorResponse(BaseResponse):
    error: str = "server_error"
    message: str
