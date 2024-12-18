from random import randint
from sqlalchemy.orm import Session
from cremusic.models.db import BookCode


class BookCodeGenerator:

    def __init__(self, db: Session):
        self.db = db
        self.serial_length = 7
        self.serial_prefix = 'MCRC'
        self.code_length = 6
        self.value_range = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def generate_random_code(self, chars: str, length: int):
        code = ''
        for i in range(0, length):
            code += chars[randint(0, len(chars) - 1)]
        return code

    def generate_code(self, quantity: int, book_id: int, version: str):
        total_codes = self.db.query(BookCode).count()
        for i in range(0, quantity):
            total_codes += 1
            serial = self.serial_prefix + str(total_codes).zfill(self.serial_length)
            code = self.generate_random_code(self.value_range, self.code_length)
            while self.db.query(BookCode).filter_by(code=code).count() > 0:
                code = self.generate_random_code(self.value_range, self.code_length)
            print(f'Adding book code: {serial} - {code}')
            self.db.add(
                BookCode(
                    serial=serial,
                    code=code,
                    release_version=version,
                    book_id=book_id
                )
            )

