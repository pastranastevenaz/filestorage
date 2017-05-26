import os
import jose from jwt
import datetime from datetime
import rethinkdb as r
from passlib.hash import pbkdf2_sha256

from flask import current_app

from api.utils.errors import ValidationError

conn=r.connect(db='papers')

class RethinkDBModel(object):
    pass

class User(RethinkDBModel):
    _table = 'users'

    @classmethod
    def create(cls, **kwargs):
        fullname = kwargs.get('fullname')
        email = kwargs.get('email')
        password = kwargs.get('password')
        password_conf = kwargs.get('password_conf')
        if password != password_conf:
            raise ValidationError('Passwords did not match!')
        password = cls.hash_password(password)
        doc = {
            'fullname': fullname,
            'email': email,
            'password': password,
            'date_created': datetime.now(r.make_timezone('+01:00')),
            'date_modified': datetime.now(r.make_timezone('+01:00'))
        }
        r.table(cls._table).insert(doc).run(conn)

    @classmethod
    def validate(cls, email, password):
        docs = list(r.table(cls._table).filter({'email': email}).run(conn))

        if not len(docs):
            raise ValidationError('Email not found')

        _hash = docs[0]['password']

        if cls.verify_password(password, _hash):
            try:
                token = jwt.encode({'id': docs[0]['id']}, current_app.config['SECRET_KEY'], algorithm='HS256')
                return token
            except JWTError:
                raise ValidationError('Problem while creating JWT Token')
        else:
            raise ValidationError('Incorrect Password')

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    @staticmethod
    def verify_password(password, _hash):
        return pbkdf2_sha256.verify(password, _hash)
