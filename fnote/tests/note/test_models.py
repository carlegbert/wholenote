from fnote.blueprints.note.models import Note
from fnote.blueprints.user.models import User


class TestNote(object):
    def test_save_to_db(self, db, user, session):
        note_num = len(Note.query.all())
        Note(user.id, 'test_note', 'note text').save()
        new_note_num = len(Note.query.all())
        assert new_note_num == note_num + 1

    def test_find_by_id(self, db, user, note):
        found_note = Note.find_by_id(note.id)
        assert note == found_note

    def test_update_title(self, db, note, session):
        new_title = 'new_title'
        note.update_title(new_title)
        assert note.title == new_title

    def test_update_text(self, db, note, session):
        new_text = 'new note text'
        note.update_text(new_text)
        assert note.text == new_text

    def test_delete_note(self, db, note, session):
        nid = note.id
        note_num = len(Note.query.all())
        note.delete()
        new_note_num = len(Note.query.all())
        found_note = Note.find_by_id(nid)
        assert new_note_num == note_num - 1
        assert not found_note

    def test_get_user_notes(self, db, user, note, session):
        note_two = Note(user.id, 'test_note', 'note text').save()
        notes = user.get_notes()
        note_num = len(notes)
        assert note_num == 2
        assert note in notes
        assert note_two in notes

    def test_get_dict(self, db, user, note):
        data = note.to_dict()
        assert data
        assert data['owner'] == user.email
        assert data['text'] == note.text
        assert data['title'] == note.title
        assert data['id'] == note.id
