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


class Video(BaseResponse):
    id: int
    book_episode_id: int
    name: str
    link: str | None
    video_id: str | None
    thumbnail: str
    duration: int
    unlocked: bool = False

    class Config:
        orm_mode = True


class PaginatedVideos(BaseResponse):
    next_token: int
    data: list[Video]


class PaginatedEpisodes(BaseResponse):
    next_token: int
    data: list[Episode]


class AboutResp(BaseResponse):
    _defaults = {
        "telephone": "19001009",
        "email": "support.cremussic@gmail.com",
        "address": "Số 7, ngõ Hội Phụ - Đông Hội - Đông Anh - Hà Nội"
    }
    telephone: str = _defaults["telephone"]
    email: str = _defaults["email"]
    address: str = _defaults["address"]



class NotFountResponse(BaseResponse):
    code: str = "not_found"
    messages: list[str] = ["Resource not found"]


class ServerErrorResponse(BaseResponse):
    code: str = "server_error"
    messages: list[str] = ["Internal server error"]


class ForbiddenResponse(BaseResponse):
    code: str = "forbidden"
    messages: list[str] = ["Forbidden"]
