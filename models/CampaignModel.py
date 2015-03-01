# -*- coding: utf-8 -*-

import logging

import re

from os import urandom
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, String
from models import dbsession, Permission
from models.BaseModels import DatabaseObject, generate_uuid

class Campaign(DatabaseObject):
	_name = Column(Unicode(32), nullable=False)
	_description = Column(Unicode(254))
	uuid = Column(String(32), unique=True, default=generate_uuid)

	user_id = Column(Integer,
		ForeignKey('user.id'),
		nullable=False,
	)	

	targets = relationship("Target",
		backref=backref("campaign", lazy="select"),
		cascade="all, delete-orphan",
	)

	endpoint = relationship("Endpoint",
		backref=backref("campaign", lazy="select"),
		cascade="all, delete-orphan",
	)

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
        self._description = value[:254]

    def to_dict(self):
    	return {
    		'uuid': str(self.uuid),
    		'name': str(self.name),
    		'description': str(self.description),
    	}
