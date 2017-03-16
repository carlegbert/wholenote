from sqlalchemy import ForeignKey
from fnote.extensions import db


class Note(db.Model):

    """Text object, belonging to a single user."""

    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())

    def __init__(self, user_id, title='New Note', text=''):
        self.user_id = user_id
        self.title = title
        self.text = text

    def save(self):
        """Save note to database.
        :return: self
        """
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

    def update_title(self, new_title):
        """ Change title of note
        :new_title: String
        :returns: Self
        """
        self.title = new_title
        db.session.add(self)
        db.session.commit()
        return self

    def update_text(self, new_text):
        """Update text of note
        :new_text: String
        :returns: Self
        """
        self.text = new_text
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Remove from database
        :returns: None
        """
        db.session.delete(self)
        db.session.commit()
