from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from fnote.extensions import db
from fnote.extensions import hashids


class Note(db.Model):

    """Text object, belonging to a single user.
    The 'hashid' is a short string that serves as the client-facing
    id. It exists to obfuscate primary keys, not to provide any significant
    security. It isn't saved to the database."""

    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    user = relationship('User')
    last_modified = db.Column(db.DateTime())

    def __init__(self, user_id, title='New Note', text=''):
        self.user_id = user_id
        self.title = title
        self.text = text

    def save(self):
        """Save note to database.
        :return: self
        """
        self.last_modified = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

        return self

    @classmethod
    def find_by_id(cls, id):
        """Find note in database by id
        :param id:
        :type id: int
        :return: Note object
        """
        return Note.query.filter(Note.id == id).first()

    @classmethod
    def find_by_hash_id(self, hash_id):
        """Decode hash_id for faster database lookup
        :returns: Note object
        """
        id = hashids.decode(hash_id)
        return Note.find_by_id(id)

    @classmethod
    def find_by_title(self, title, user):
        """Retrieve note owned by <user> named <title>"""
        return Note.query.filter(Note.user == user) \
                         .filter(Note.title == title) \
                         .first()

    def update_title(self, new_title):
        """ Change title of note
        :new_title: String
        :returns: Self
        """
        self.title = new_title
        self.last_modified = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return self

    def update_text(self, new_text):
        """Update text of note
        :new_text: String
        :returns: Self
        """
        self.text = new_text
        self.last_modified = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Remove from database
        :returns: None
        """
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        data = {'title': self.title,
                'text': self.text,
                'owner': self.user.email,
                'id': hashids.encode(self.id),
                'lastModified': self.last_modified,
                }
        return data

    def find_matching_titles(self):
        matches = Note.query.filter(Note.owner == self.owner) \
                            .filter(Note.title == self.title)
        return len(matches)
