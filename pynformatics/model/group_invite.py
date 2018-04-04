from sqlalchemy import (
    Column,
    ForeignKey,
)
from sqlalchemy.orm import (
    backref,
    relationship,
)
from sqlalchemy.types import (
    Boolean,
    Enum,
    Integer,
)

from pynformatics.model.meta import Base
from pynformatics.models import DBSession
from pynformatics.utils.exceptions import GroupNotFound
from pynformatics.utils.functions import attrs_to_dict
from pynformatics.utils.url_encoder import (
    decode,
    encode,
)


class GroupInvite(Base):
    __table_args__ = {'schema': 'pynformatics'}
    __tablename__ = 'group_invite'

    REDIRECT_COURSE = 'COURSE'
    REDIRECT_STATEMENT = 'STATEMENT'
    REDIRECT_TYPES = [
        REDIRECT_COURSE,
        REDIRECT_STATEMENT,
    ]

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_group.id')) # int(11)
    creator_id = Column(Integer, ForeignKey('moodle.mdl_user.id')) # bigint(11) unsigned
    redirect_type = Column(Enum(*REDIRECT_TYPES))
    instance_id = Column(Integer) # bigint(10) unsigned
    disabled = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    group = relationship('Group', backref='group_invites', lazy='joined')
    creator = relationship('SimpleUser', backref='group_invites', lazy='joined')

    @property
    def redirect(self):
        if self.redirect_type == GroupInvite.REDIRECT_COURSE:
            return {'course_id': self.instance_id}
        elif self.redirect_type == GroupInvite.REDIRECT_STATEMENT:
            return {'statement_id': self.instance_id}
        else:
            raise NotImplementedError

    @property
    def url(self):
        return encode(self.id)

    @staticmethod
    def get_by_url(url):
        try:
            id = decode(url)
        except Exception:
            raise GroupNotFound

        group = DBSession.query(GroupInvite).filter_by(id=id).first()
        if not group:
            raise GroupNotFound
        return group

    def serialize(self, context, attributes=None):
        if attributes is None:
            attributes = (
                'group_id',
                'creator_id',
                'redirect',
                'disabled',
                'url'
            )
        serialized = attrs_to_dict(self, *attributes)
        return serialized
