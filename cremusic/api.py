from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from cremusic.models import req, resp, db
from cremusic.db import get_session

api_router = APIRouter(prefix="/v1")
index_router = APIRouter()


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
                db.StatisticLog(
                    telephone=body.telephone,
                    code=code,
                    name=body.name,
                )
            )
        ses.commit()
    return resp.CheckBookCodeResponse(
        valid=book_code_exists,
    )


@api_router.get("/books", response_model=resp.PaginatedBooks)
def get_books(
    paging: req.ListBookPaginatorReq = Depends(req.ListBookPaginatorReq),
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
def get_book_videos(book_id: int):
    """Get videos by book id"""
    pass


@api_router.get("/books/{book_id}/episodes")
def get_book_episodes(book_id: int):
    """Get episodes by book id"""
    pass


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
