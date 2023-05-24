from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from cremusic.models import req, resp, db
from cremusic.db import get_session

api_router = APIRouter(prefix="/v1")
index_router = APIRouter()


def get_global_config(ses: Session):
    # get global config
    config = ses.execute(
        select(db.BookCodeConfig).limit(1)
    ).scalar()
    if not config:
        raise HTTPException(
            status_code=500,
            detail=resp.ServerErrorResponse(
                messages=["Global config not found"]
            ).dict()
        )
    return config


def get_book(ses: Session, book_id: int):
    book = ses.execute(
        select(db.Book).where(db.Book.id == book_id)
    ).scalar()
    if not book:
        raise HTTPException(
            status_code=404,
            detail=resp.NotFountResponse(
                messages=[f"Book {book_id} not found"]
            ).dict()
        )
    return book


def check_book_code(ses, book_id: int, book_code: str):
    # check if book code is valid
    book_code_exists = ses.execute(
        select(db.BookCode.id)
        .filter(
            db.BookCode.code == book_code,
            db.BookCode.book_id == book_id
        )
        .limit(1)
    ).scalar()
    if not book_code_exists:
        raise HTTPException(
            status_code=404,
            detail=resp.NotFountResponse(
                messages=[f"Book code {book_code} not found"]
            ).dict()
        )


@index_router.get("/tokenInfo")
def get_token_info():
    """Get token info"""
    pass


@index_router.get("/")
def get_index():
    """Get index"""
    pass


@api_router.post("/book/book-code", response_model=resp.CheckBookCodeResponse)
def book_code(
    body: req.VerifyCodeRequest = Depends(req.VerifyCodeRequest),
    ses: Session = Depends(get_session),
):
    """Check code of book and update statistics"""
    code = body.book_code
    book_id = body.book_id
    book_code_exists = (
        ses.query(db.BookCode)
        .where(db.BookCode.code == code, db.BookCode.book_id == book_id)
        .exists()
        .scalar()
    )
    if book_code_exists:
        # find existing by telephone and code
        ses.begin()
        obj = ses.query(
            db.StatisticLog.telephone == body.telephone,
            db.StatisticLog.code == code
        ).first()
        if obj:
            # update
            if not obj.telephone:
                obj.telephone = body.telephone
            if not obj.code:
                obj.code = code
            ses.add(obj)
        else:
            # create new
            ses.add(
                db.StatisticLog(telephone=body.telephone, code=code, name=body.name) # type: ignore
            )
        ses.commit()
    return resp.CheckBookCodeResponse(
        valid=book_code_exists,
    )


@api_router.get("/books", response_model=resp.PaginatedBooks)
def get_books(
    paging: req.PaginationParams = Depends(req.PaginationParams),
    ses: Session = Depends(get_session),
):
    """Get all books"""
    next_id = paging.next_token
    limit = paging.limit
    query = (
        select(db.Book)
        .where(db.Book.id > next_id)
        .limit(limit)
        .order_by(db.Book.id.asc())
    )
    books = ses.execute(query).scalars().all()
    return resp.PaginatedBooks(
        next_token=books[-1].id if books else 0,
        required_unlock=False,
        data=[resp.Book.from_orm(book) for book in books],
    )


@api_router.get("/books/{book_id}/videos")
def get_book_videos(
    book_id: int,
    query: req.PaginationWithBookCode = Depends(req.PaginationWithBookCode),
    ses: Session = Depends(get_session),
):
    """Get videos by book id"""
    # get the book by book id
    get_book(ses, book_id)
    # get global config
    config = get_global_config(ses)

    # if book code is provided, check if it is valid
    if query.book_code:
        if config.required_unlock or config.global_code != query.book_code:
            # check if book code is valid
            check_book_code(ses, book_id, query.book_code)
    # list episodes by book id
    # count total videos of each episode
    videos = (
        ses.query(
            db.Video,
        )
        .join(db.Episode, db.Episode.id == db.Video.book_episode_id, isouter=True)
        .where(
            db.Episode.book_id == book_id,
            db.Video.id > query.next_token,
        )
        .order_by(db.Video.id.asc())
        .limit(query.limit)
        .all()
    )

    unlocked = bool(query.book_code)
    paginated_data = []
    for video in videos:
        video.unlocked = unlocked
        if not unlocked:
            video.link = None
            video.video_id = None
        paginated_data.append(resp.Video.from_orm(video))
    return resp.PaginatedVideos(
        next_token=videos[-1].id if videos else 0,
        data=paginated_data,
    )


@api_router.get("/books/{book_id}/episodes", response_model=resp.PaginatedEpisodes)
def get_book_episodes(
    book_id: int,
    query: req.PaginationWithBookCode = Depends(req.PaginationWithBookCode),
    ses: Session = Depends(get_session),
):
    """Get episodes by book id"""
    # get the book by book id
    get_book(ses, book_id)
    # get global config
    config = get_global_config(ses)

    # FIXME: bellow seems incorrect, it should be if the book is required to unlock,
    # then check if the book code is provided and valid

    # if book code is provided, check if it is valid
    if query.book_code:
        if config.required_unlock or config.global_code != query.book_code:
            # check if book code is valid
            check_book_code(ses, book_id, query.book_code)
    # list episodes by book id
    # count total videos of each episode
    episodes = (
        ses.query(
            db.Episode,
            func.count(db.Video.id).label("total_videos"),
        )
        .group_by(db.Episode.id)
        .where(
            db.Episode.book_id == book_id,
            db.Episode.id > query.next_token,
        )
        .order_by(db.Episode.id.asc())
        .limit(query.limit)
        .all()
    )

    unlocked = bool(query.book_code)
    paginated_data = []
    for episode, total_videos in episodes:
        episode.total_videos = total_videos
        episode.unlocked = unlocked
        paginated_data.append(resp.Episode.from_orm(episode))
    return resp.PaginatedEpisodes(
        next_token=episodes[-1][0].id if episodes else 0,
        data=paginated_data,
    )



@api_router.post("/admin/config")
def admin_config(body: req.BookCodeConfigReq):
    pass


@api_router.get("/episodes/{episode_id}/videos")
def get_episode_videos(episode_id: int):
    """Get videos by episode id"""
    pass


@api_router.get("/contact")
def get_contact():
    """Get contact info"""
    pass
