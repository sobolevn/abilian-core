"""
Activity Service.

See: http://activitystrea.ms/specs/json/1.0/
See: http://activitystrea.ms/specs/atom/1.0/#activity
See: http://stackoverflow.com/questions/1443960/how-to-implement-the-activity-stream-in-a-social-network

TODO: replace `subject` by `target`. Also look wether other attributes from
the spec need to be implemented.
"""

from datetime import datetime
from flask import logging

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, DateTime, Text, String

from abilian.core.entities import db, Entity
from abilian.core.subjects import User

__all__ = ['ActivityEntry']

logger = logging.getLogger(__name__)

class ActivityEntry(db.Model):
  """Main table for all activities."""

  id = Column(Integer, primary_key=True)
  happened_at = Column(DateTime, default=datetime.utcnow)

  verb = Column(Text)

  actor_id = Column(Integer, ForeignKey(User.id))
  actor = relationship(User, foreign_keys=actor_id)

  object_type = Column(String(1000))
  object_id = Column(Integer)
  _fk_object_id = Column(Integer, ForeignKey(Entity.id, ondelete="SET NULL"))
  object = relationship(Entity, foreign_keys=_fk_object_id)

  target_type = Column(String(1000))
  target_id = Column(Integer)
  _fk_target_id = Column(Integer, ForeignKey(Entity.id, ondelete="SET NULL"))
  target = relationship(Entity, foreign_keys=_fk_target_id)

  def __repr__(self):
    return '<%s.ActivityEntry id=%s actor="%s" verb="%s" object="%s" target="%s">' % (
      self.__class__.__module__, self.id,
      unicode(self.actor).encode('utf-8'),
      self.verb,
      unicode(self.object).encode('utf-8'),
      unicode(self.target).encode('utf-8'))
