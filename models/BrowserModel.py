# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.types import String
from sqlalchemy.orm import relationship, backref
from models import dbsession
from models.BaseModels import DatabaseObject, generate_uuid


class Browser(DatabaseObject):

    uuid = Column(String(32), unique=True, default=generate_uuid)

    _name = Column(String(32))
    _version = Column(String(32))
    _codename = Column(String(32))
    _platform = Column(String(32))
    _user_agent = Column(String(64))
    _oscpu = Column(String(32))

    # Belongs to Target
    target_id = Column(Integer, ForeignKey('target.id'), nullable=False)

    # Has many Plugins
    plugins = relationship("Plugin",
                           backref=backref("browser", lazy="select"),
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

    # Properties

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value[:32])

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = str(value[:32])

    @property
    def codename(self):
        return self._codename

    @codename.setter
    def codename(self, value):
        self._codename = str(value[:32])

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, value):
        self._platform = str(value[:32])

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        self._user_agent = str(value[:64])

    @property
    def oscpu(self):
        return self._oscpu

    @oscpu.setter
    def oscpu(self, value):
        self._oscpu = str(value[:32])