from datetime import datetime
import re

from sqlalchemy import ForeignKey, exc
from sqlalchemy.orm import relationship
from fnote.extensions import db
from fnote.extensions import hashids


class Note(db.Model):

    """Text object, belonging to a single user.

    title_id is a unique identifier that allows a descriptive, human-readable,
    url-friendly string to be used as a key to retrieve a note. The note can
    have a title that is non-unique and has special characters, but the
    'cleaned' title will be used to retrieve notes.

    The 'hashid' is a short string that serves as the client-facing
    id. It exists to obfuscate primary keys, not to provide any significant
    security. It isn't saved to the database. Currently it is not used for
    anything, but it may be useful in the future if a non-changing identifier
    is needed (title_id will always be unique, but since titles are changeable
    it is not necessarily unchanging."""

    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    title = db.Column(db.String(255), nullable=False)
    clean_title = db.Column(db.String(255), nullable=False)
    title_id = db.Column(db.String(255), nullable=False, unique=True)
    text = db.Column(db.Text())
    user = relationship('User')
    last_modified = db.Column(db.DateTime())

    def __init__(self, user_id, title='New Note', text=''):
        self.user_id = user_id
        self.title = title
        self.text = text
        self.title_id = Note.clean_title(title)

    def save(self):
        """Save note to database.
        :return: self
        """
        try:
            self.last_modified = datetime.utcnow()
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            self.number_title_id(self.title)

        return self

    @classmethod
    def clean_title(cls, title):
        """Remove URL-unfriendly characters from string"""
        regexp = r'[^A-Za-z0-9_.~-]'
        return re.sub(regexp, '', title)

    @classmethod
    def find_by_id(cls, id):
        """Find note in database by id
        :param id:
        :type id: int
        :return: Note object
        """
        return Note.query.filter(Note.id == id).first()

    @classmethod
    def find_by_hash_id(cls, hash_id):
        """Decode hash_id for faster database lookup
        :returns: Note object
        """
        id = hashids.decode(hash_id)
        return Note.find_by_id(id)

    @classmethod
    def find_by_title_id(cls, title_id, user):
        """Retrieve note owned by <user> named <title>"""
        return Note.query.filter(Note.user == user) \
                         .filter(Note.title_id == title_id) \
                         .first()

    def update(self, text=None, title=None):
        """ Change title and text of note
        :new_title: String
        :returns: Self
        """
        if text is not None and self.text != text:
            self.text = text
            db.session.add(self)
            self.last_modified = datetime.utcnow()

        if title is not None and self.title != title:
            self.title = title
            self.title_id = Note.clean_title(title)
            self.last_modified = datetime.utcnow()
            try:
                db.session.add(self)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                self.number_title_id(title)
        return self

    def delete(self):
        """Remove from database
        :returns: None
        """
        db.session.delete(self)
        db.session.commit()

    def number_title_id(self, title, attempts=1):
        """In case an attempt is made to create a note with an identical
        title_id, we need to stick a number on the end. This function
        recursively calls itself until it succeeds.  """
        # TODO: instead of using recursion, use a SQL statement with regex

        try:
            self.title = title
            self.title_id = Note.clean_title(title) + str(attempts+1)
            db.session.add(self)
            db.session.commit()
            return None
        except exc.IntegrityError:
            db.session.rollback()
            attempts += 1
            self.number_title_id(title, attempts)

    def to_dict(self):
        data = {'title': self.title,
                'text': self.text,
                'owner': self.user.email,
                'id': self.title_id,
                'lastModified': self.last_modified,
                }
        return data
