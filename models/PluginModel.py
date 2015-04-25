# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.types import String
from sqlalchemy.orm import relationship, backref
from models import dbsession
from models.BaseModels import DatabaseObject, generate_uuid


class Plugin(DatabaseObject):
    """
    A Plugin represents a browser plugin
    """

    uuid = Column(String(32), unique=True, default=generate_uuid)

    _name = Column(String(64))
    _description = Column(String(128))
    _version = Column(String(32))

    # belongs_to browser
    browser_id = Column(Integer, ForeignKey('browser.id'), nullable=False)
    browser = relationship("Browser", backref=backref("plugin", lazy="select"))

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
        self._name = str(value[:64])

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = str(value[:128])

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = str(value[:32])

    def to_dict(self):
        return {
            'uuid': str(self.uuid),
            'name': str(self.name),
            'version': str(self._version),
            'description': str(self._description),
        }