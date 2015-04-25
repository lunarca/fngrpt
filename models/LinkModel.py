# -*- coding: utf-8 -*-

import logging
import re
import string
import random

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, String
from models import dbsession, Permission
from models.BaseModels import DatabaseObject, generate_uuid

from os import urandom


class Link(DatabaseObject):
    '''
    A Link is a mapping between a Target and an Endpoint. This is the
    part that actually directs the user to the endpoint

    It's the part that goes like fngr.pt/s?l=14sdfja
    '''

    # Code to generate a random 8 character string
    generate_dispid = lambda:''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for _ in range(8))

    uuid = Column(String(32), unique=True, default=generate_uuid)

    display_id = Column(String(8), unique=True, default=generate_dispid)

    endpoint_id = Column(Integer, ForeignKey('endpoint.id'),
                         nullable=False,)

    target_id = Column(Integer, ForeignKey('target.id'),
                       nullable=False,)

    @classmethod
    def all(cls):
        return dbsession.query(cls).all()

    @classmethod
    def by_id(cls, _id):
        return dbsession.query(cls).filter_by(id=_id).first()

    @classmethod
    def by_uuid(cls, _uuid):
        return dbsession.query(cls).filter_by(uuid=_uuid).first()

    @classmethod
    def by_display_id(cls, _dispid):
        return dbsession.query(cls).filter_by(display_id=_dispid).first()

    def to_dict(self):
        return {
            'uuid': str(self.uuid),
            'display_id': str(self.display_id)
        }

