# -*- coding: utf-8 -*-

import logging

import re

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, String
from models import dbsession, Permission
from models.BaseModels import DatabaseObject, generate_uuid


class Campaign(DatabaseObject):
    _name = Column(Unicode(32), nullable=False)
    _description = Column(Unicode(256))
    uuid = Column(String(32), unique=True, default=generate_uuid)
    _endpoint = Column(Unicode(256))

    user_id = Column(Integer,
                     ForeignKey('user.id'),
                     nullable=False,
                     )

    user = relationship("User", backref=backref("campaign", lazy="select"))

    @classmethod
    def all(cls):
        return dbsession.query(cls).all()

    @classmethod
    def by_id(cls, _id):
        return dbsession.query(cls).filter_by(id=_id).first()

    @classmethod
    def by_uuid(cls, _uuid):
        return dbsession.query(cls).filter_by(uuid=_uuid).first()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value[:32]

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value[:256]

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = unicode(value[:256])

    def to_dict(self):
        return {
            'uuid': str(self.uuid),
            'name': str(self.name),
            'description': str(self.description),
        }
