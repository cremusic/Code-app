from typing import overload
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from cremusic.models import req, resp, db
from cremusic.db import get_session, autocommit

api_router = APIRouter(prefix="/v1")
index_router = APIRouter()


@overload
def get_global_config(ses: Session, raise_on_not_found=True) -> db.BookCodeConfig:
    ...


@overload
def get_global_config(ses: Session, raise_on_not_found=False) -> db.BookCodeConfig | None:
    ...


def get_global_config(ses: Session, raise_on_not_found: bool=True):
    # get global config
    config = ses.execute(select(db.BookCodeConfig).limit(1)).scalar()
    if not config:
        if raise_on_not_found:
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


def get_episode(ses: Session, episode_id: int):
    ep = ses.execute(
        select(db.Episode).where(db.Episode.id == episode_id)
    ).scalar()
    if not ep:
        raise HTTPException(
            status_code=404,
            detail=resp.NotFountResponse(
                messages=[f"Episode {episode_id} not found"]
            ).dict()
        )
    return ep


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


def check_book_unlocked(
    ses: Session, config: db.BookCodeConfig, book: db.Book, book_code: str | None
) -> bool:
    # book may have not_require_unlock flag set to true, in this case,
    # book code is not required (ignore global config)
    unlocked = False
    if book.not_require_unlock:
        unlocked = True
    else:
        # if book code is provided, check if it is valid
        if book_code:
            if config.required_unlock or config.global_code != book_code:
                # check if book code is valid
                check_book_code(ses, book.id, book_code)
            unlocked = True
    return unlocked


def get_paginated_video_resp(
    videos: list[db.Video],
    unlocked: bool,
):
    paginated_data: list[resp.Video] = []
    for video in videos:
        obj = resp.Video.from_orm(video)
        obj.unlocked = unlocked
        if not unlocked:
            obj.link = None
            obj.video_id = None
        paginated_data.append(obj)
    return resp.PaginatedVideos(
        next_token=paginated_data[-1].id if paginated_data else 0,
        data=paginated_data,
    )


@index_router.get("/tokenInfo")
def get_token_info():
    """Get token info"""
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
        ses.query(db.BookCode.id)
        .where(db.BookCode.code == code, db.BookCode.book_id == book_id)
        .limit(1)
        .scalar()
    )
    if book_code_exists:
        # find existing by telephone and code
        obj = ses.execute(
            select(db.StatisticLog)
            .where(
                db.StatisticLog.telephone == body.telephone,
                db.StatisticLog.code == code
            )
            .limit(1)
        ).scalar()
        with autocommit(ses):
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
                    db.StatisticLog(
                        telephone=body.telephone,
                        code=code,
                        name=body.name
                    )
                )
    return resp.CheckBookCodeResponse(valid=bool(book_code_exists))


@api_router.post("/admin/config")
def admin_config(
    body: req.BookCodeConfigReq,
    ses: Session = Depends(get_session),
):
    config = get_global_config(ses)
    if config.secret != body.secret:
        raise HTTPException(
            status_code=403,
            detail=resp.ForbiddenResponse(
                messages=["Invalid secret"]
            ).dict()
        )
    if body.global_code:
        config.global_code = body.global_code
    if body.required_unlock is not None:
        config.required_unlock = body.required_unlock
    with autocommit(ses):
        ses.add(config)
    return JSONResponse(status_code=204, content=None)


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
    config = get_global_config(ses, raise_on_not_found=False)
    if config:
        required_unlock = bool(config.required_unlock)
    else:
        required_unlock = False
    return resp.PaginatedBooks(
        next_token=books[-1].id if books else 0,
        required_unlock=required_unlock,
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
    book = get_book(ses, book_id)
    # get global config
    config = get_global_config(ses)

    video_unlocked = check_book_unlocked(ses, config, book, query.book_code)

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
    return get_paginated_video_resp(videos, video_unlocked)


@api_router.get("/episodes/{episode_id}/videos")
def get_episode_videos(
    episode_id: int,
    query: req.PaginationWithBookCode = Depends(req.PaginationWithBookCode),
    ses: Session = Depends(get_session),
):
    """Get videos by episode id"""
    episode = get_episode(ses, episode_id)
    # get global config
    config = get_global_config(ses)

    video_unlocked = check_book_unlocked(ses, config, episode.book, query.book_code)
    # list episodes by book id
    # count total videos of each episode
    videos = (
        ses.query(db.Video)
        .where(
            db.Video.book_episode_id == episode_id,
            db.Video.id > query.next_token,
        )
        .order_by(db.Video.id.asc())
        .limit(query.limit)
        .all()
    )
    return get_paginated_video_resp(videos, video_unlocked)


@api_router.get("/books/{book_id}/episodes", response_model=resp.PaginatedEpisodes)
def get_book_episodes(
    book_id: int,
    query: req.PaginationWithBookCode = Depends(req.PaginationWithBookCode),
    ses: Session = Depends(get_session),
):
    """Get episodes by book id"""
    # get the book by book id
    book = get_book(ses, book_id)
    # get global config
    config = get_global_config(ses)

    unlocked = check_book_unlocked(ses, config, book, query.book_code)
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

    paginated_data = []
    for episode, total_videos in episodes:
        episode.total_videos = total_videos
        episode.unlocked = unlocked
        paginated_data.append(resp.Episode.from_orm(episode))
    return resp.PaginatedEpisodes(
        next_token=episodes[-1][0].id if episodes else 0,
        data=paginated_data,
    )


@api_router.get("/contact")
def get_contact() -> resp.AboutResp:
    """Get contact info"""
    return resp.AboutResp()
