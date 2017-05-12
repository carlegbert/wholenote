from fnote.blueprints.note.models import Note
from fnote.blueprints.user.models import User
from fnote.extensions import hashids


class TestNote(object):
    def test_save_to_db(self, user, session):
        note_num = len(Note.query.all())
        Note(user.id, 'test_note_2', 'note text').save()
        new_note_num = len(Note.query.all())
        assert new_note_num == note_num + 1

    def test_find_by_id(self, user, note):
        found_note = Note.find_by_id(note.id)
        assert note == found_note

    def test_find_by_hashid(self, user, session, note):
        hash_id = hashids.encode(note.id)
        found_note = Note.find_by_hash_id(hash_id)
        assert note == found_note

    def test_find_by_titleid(self, user, session, note):
        found_note = Note.find_by_title_id(note.title_id, user)
        assert note == found_note

    def test_find_by_titleid_fails(self, user):
        found_note = Note.find_by_title_id('nonexistent_note', user)
        assert found_note is None

    def test_update_title(self, note, session):
        new_title = 'new_title'
        note.update(title=new_title)
        assert note.title == new_title
        assert note.title_id == new_title

    def test_update_text(self, note, session):
        new_text = 'new note text'
        note.update(text=new_text)

    def test_delete_note(self, note, session):
        nid = note.id
        note_num = len(Note.query.all())
        note.delete()
        new_note_num = len(Note.query.all())
        found_note = Note.find_by_id(nid)
        assert new_note_num == note_num - 1
        assert not found_note

    def test_get_user_notes(self, user, note, session):
        note_two = Note(user.id, 'test_note_2', 'note text').save()
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

    def test_update_changes_date(self, note):
        old_dt = note.last_modified
        note.update(title='new_title')
        new_dt = note.last_modified
        assert new_dt != old_dt

    def test_titleid_cleaned(self, user, session):
        n = Note(user.id, title='New_!@#$%%^&*()123"\';:<>[]{}\\|`/ Note')
        assert n.title_id == 'New_123Note'

    def test_calculate_titleid(self, user, session):
        n1 = Note(user.id, title='test_titleid').save()
        n2 = Note(user.id, title='test_titleid').save()
        assert n1.title_id == 'test_titleid'
        assert n2.title_id == 'test_titleid_2'

    def test_calculate_10_same_title(self, user, session):
        for i in range(9):
            Note(user.id, title='many_same_title').save()
        last_note = Note(user.id, title='many_same_title').save()
        assert last_note.title_id == 'many_same_title_10'

    def test_sametitleid_diffuser(self, user, session):
        u2 = User.register(email='othertestuser@localhost', password='x'*10)
        n1 = Note(user.id, 'diffuser').save()
        n2 = Note(u2.id, 'diffuser').save()
        assert n1.title_id == n2.title_id

    def test_titleid_wrong_user(self, user, session, note):
        note = Note(user.id, title='wronguser', text='').save()
        u2 = User.register(email='wrongusertest@localhost', password='x'*10)
        u1_found_note = Note.find_by_title_id(note.title_id, user)
        u2_found_note = Note.find_by_title_id('wronguser', u2)
        assert u1_found_note == note
        assert u2_found_note is None
