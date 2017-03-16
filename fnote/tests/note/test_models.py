from fnote.blueprints.note.models import Note
from fnote.blueprints.user.models import User


class TestNote(object):
    def test_save_to_db(self, db):
        u = User.register(email='note_tester@localhost', password='hunter2')
        note_num = len(Note.query.all())
        Note(u.id, 'test_note', 'note text').save()
        new_note_num = len(Note.query.all())
        assert new_note_num == note_num + 1

    def test_find_by_id(self, db):
        u = User.register(email='note_tester2@localhost', password='hunter2')
        note = Note(u.id, 'test_note', 'note text').save()
        found_note = Note.find_by_id(note.id)
        assert note == found_note

    def test_update_title(self, db):
        u = User.register(email='note_tester3@localhost', password='hunter2')
        note = Note(u.id, 'test_note', 'note text').save()
        new_title = 'new_title'
        note.update_title(new_title)
        assert note.title == new_title

    def test_update_text(self, db):
        u = User.register(email='note_tester4@localhost', password='hunter2')
        note = Note(u.id, 'test_note', 'note text').save()
        new_text = 'new note text'
        note.update_text(new_text)
        assert note.text == new_text

    def test_delete_note(self, db):
        u = User.register(email='note_tester5@localhost', password='hunter2')
        note = Note(u.id, 'test_note', 'note text').save()
        nid = note.id
        note_num = len(Note.query.all())
        note.delete()
        new_note_num = len(Note.query.all())
        found_note = Note.find_by_id(nid)
        assert new_note_num == note_num - 1
        assert not found_note

    def test_get_user_notes(self, db):
        u = User.register(email='note_tester6@localhost', password='hunter2')
        note_one = Note(u.id, 'test_note', 'note text').save()
        note_two = Note(u.id, 'test_note', 'note text').save()
        notes = u.get_notes()
        note_num = len(notes)
        assert note_num == 2
        assert note_one in notes
        assert note_two in notes
