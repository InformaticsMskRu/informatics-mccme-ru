"""Group model"""
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Integer, Unicode

from pynformatics.model.meta import Base
from pynformatics.utils.functions import attrs_to_dict


class Group(Base):
    __tablename__ = "mdl_ejudge_group"
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)
    owner_id = Column(Integer)
    visible = Column(Integer)

    def serialize(self):
        return attrs_to_dict(
            self,
            'id',
            'name',
            'description',
            'owner_id',
            'visible'
        )


class UserGroup(Base):
    __tablename__ = "mdl_ejudge_group_users"
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("moodle.mdl_user.id"))
    group_id = Column(Integer, ForeignKey("moodle.mdl_ejudge_group.id"))

    group = relationship("Group", backref=backref("UserGroup", lazy="select"))
    user = relationship("User", backref=backref("UserGroup", lazy="select"))

    # firstname = association_proxy('user', 'firstname')
    # lastname = association_proxy('user', 'lastname')
    # deleted = association_proxy('user', 'deleted')
    # problems_solved = association_proxy('user', 'problems_solved')
    # ejudge_id = association_proxy('user', 'ejudge_id')
    # city = association_proxy('user', 'city')
    # school = association_proxy('user', 'school')
