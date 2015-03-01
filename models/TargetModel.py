# -*- coding: utf-8 -*-

import logging

import re

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, String
from models import dbsession, Permission
from models.BaseModels import DatabaseObject, generate_uuid

class Target(DatabaseObject):
	''' Target: A person targeted for analysis. Usually represented as an email address. '''
	_email = Column(Unicode(64), nullable=False)

	_name = Column(Unicode(32))
	uuid = Column(String(32), unique=True, default=generate_uuid)

	# belongs to Campaign
	campaign_id = Column(Integer, 
		ForeignKey('campaign.id'),
		nullable = False
	)

	# has many Browsers
	browsers = relationship("Browser", 
		backref=backref("target", lazy="select"),
		cascade="all, delete-orphan"
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

    @classmethod
    def is_email(cls, email):
        ''' Quick regex to see if the email is formatted correctly '''
        regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
        return bool(re.match(regex, email))

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = unicode(value[:32])

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
    	if not (self.is_email(value)):
    		raise ValidationError("'%s' is not a valid email address" % value)
    	self._email = unicode(value[:64])
    
    def to_dict(self):
    	return {
    		'uuid': str(self.uuid),
    		'email': str(self.email),
    		'name': str(self.name),
    	}

