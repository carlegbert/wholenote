from fnote.blueprints.note.models import Note
from fnote.extensions import hashids


class TestNote(object):
    def test_save_to_db(self, user, session):
        note_num = len(Note.query.all())
        Note(user.id, 'test_note', 'note text').save()
        new_note_num = len(Note.query.all())
        assert new_note_num == note_num + 1

    def test_find_by_id(self, user, note):
        found_note = Note.find_by_id(note.id)
        assert note == found_note

    def test_find_by_hashid(self, user, session, note):
        hash_id = hashids.encode(note.id)
        found_note = Note.find_by_hash_id(hash_id)
        assert note == found_note

    def test_find_by_title(self, user, session, note):
        found_note = Note.find_by_title(note.title, user)
        assert note == found_note

    def test_update_title(self, note, session):
        new_title = 'new_title'
        note.update_title(new_title)
        assert note.title == new_title

    def test_update_text(self, note, session):
        new_text = 'new note text'
        note.update_text(new_text)

    def test_delete_note(self, note, session):
        nid = note.id
        note_num = len(Note.query.all())
        note.delete()
        new_note_num = len(Note.query.all())
        found_note = Note.find_by_id(nid)
        assert new_note_num == note_num - 1
        assert not found_note

    def test_get_user_notes(self, user, note, session):
        note_two = Note(user.id, 'test_note', 'note text').save()
        notes = user.get_notes()
        note_num = len(notes)
        assert note_num == 2
        assert note in notes
        assert note_two in notes

    def test_get_dict(self, user, note):
        data = note.to_dict()
        assert data
        assert data['owner'] == user.email
        assert data['text'] == note.text
        assert data['title'] == note.title
        assert data['id'] == hashids.encode(note.id)

    def test_update_changes_date(self, note):
        old_dt = note.last_modified
        note.update_title('new_title')
        new_dt = note.last_modified
        assert new_dt != old_dt
