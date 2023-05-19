import pytest

from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError

from db.test_db import engine
from middleware import pereval_to_db, get_single_pereval, patch_single_pereval, get_pereval_by_email
from extentions import test_item_1, test_item_2


class TestPerevalToDB:

    def pick_db(self):
        if self.i == 1:
            if self.db:
                self.db.close()
        elif self.i == 2:
            if not self.db:
                self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def test_normal(self):
        self.i = 2
        self.pick_db()
        assert type(pereval_to_db(test_item_1, self.db)) == int

    def test_db_connection(self):
        self.i = 1
        self.pick_db()
        assert pereval_to_db(test_item_1, self.db) == 'db_error'

    def test_validation(self):
        self.i = 2
        self.pick_db()
        try:
            pereval_to_db(test_item_2, self.db)
        except ValidationError as e:
            assert e


class TestGetSinglePereval:

    def pick_db(self):
        if self.i == 1:
            if self.db:
                self.db.close()
        elif self.i == 2:
            if not self.db:
                self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def test_db_connection(self):
        self.i = 1
        self.pick_db()
        assert get_single_pereval(1, self.db) == 'db_error'

    def test_id_check(self):
        self.i = 2
        self.pick_db()
        assert get_single_pereval(25000, self.db) == 'invalid_id'

    def test_normal(self):
        self.i = 2
        self.pick_db()
        assert get_single_pereval(1, self.db)[0].id == 1


class TestPatchSinglePereval:

    def pick_db(self):
        if self.i == 1:
            if self.db:
                self.db.close()
        elif self.i == 2:
            if not self.db:
                self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def test_status(self):
        self.i = 2
        self.pick_db()
        assert patch_single_pereval(test_item_1, 2, self.db) == 'not_new'

    def test_db_connection(self):
        self.i = 1
        self.pick_db()
        assert patch_single_pereval(test_item_1, 1, self.db) == 'db_error'

    def test_validation(self):
        self.i = 2
        self.pick_db()
        try:
            patch_single_pereval(test_item_2, 1, self.db)
        except ValidationError as e:
            assert e

    def test_normal(self):
        self.i = 2
        self.pick_db()
        assert patch_single_pereval(test_item_1, 1, self.db)[0].id == 'ok'

    def test_id_check(self):
        self.i = 2
        self.pick_db()
        assert patch_single_pereval(test_item_1, 25000, self.db) == 'invalid_id'


class TestGetPerevalByEmail:

    def pick_db(self):
        if self.i == 1:
            if self.db:
                self.db.close()
        elif self.i == 2:
            if not self.db:
                self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def test_db_connection(self):
        self.i = 1
        self.pick_db()
        assert get_pereval_by_email('string', self.db) == 'db_error'

    def test_email_check(self):
        self.i = 2
        self.pick_db()
        assert get_pereval_by_email('str', self.db) == 'invalid_email'

    def test_normal(self):
        self.i = 2
        self.pick_db()
        assert get_pereval_by_email('string', self.db)[0].id == 1
