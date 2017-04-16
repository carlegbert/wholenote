/* eslint-env browser, jquery */

import {
  addNote,
  getNotes,
  deleteNote,
  selectNote,
  updateNote,
} from './actions/actions';

import {
  allNoteElements,
  newNoteForm,
  noteList,
} from './renders';


export function getNoteRequest(store) {
  const aTkn = store.getState().accessToken;
  $.ajax({
    url: 'http://localhost:9000/api/v1.0/notes',
    crossDomain: true,
    type: 'GET',
    headers: { Authorization: `Bearer ${aTkn}` },
  }).done((res) => {
    store.dispatch(getNotes(res.notes));
    allNoteElements(store);
  });
}

export function createNoteRequest(store) {
  const aTkn = store.getState().accessToken;
  const title = $('#new-title').val();
  const text = $('#new-text').val();
  const data = JSON.stringify({ title, text });

  $.ajax({
    url: 'http://localhost:9000/api/v1.0/notes',
    crossDomain: true,
    type: 'POST',
    headers: { Authorization: `Bearer ${aTkn}` },
    contentType: 'application/json',
    data,
  }).done((res) => {
    store.dispatch(addNote(res.note));
    store.dispatch(selectNote(res.note.id));
    noteList(store);
  }).fail((err) => {
    console.log('failure');
  });
}

export function updateNoteRequest(store) {
  const title = $('#update-title').val();
  const text = $('#update-text').val();
  const data = JSON.stringify({ title, text });
  const aTkn = store.getState().accessToken;
  const id = store.getState().selectedNote.id;
  $.ajax({
    url: `http://localhost:9000/api/v1.0/notes/${id}`,
    crossDomain: true,
    type: 'PUT',
    headers: { Authorization: `Bearer ${aTkn}` },
    contentType: 'application/json',
    data,
  }).done((res) => {
    const oldTitle = store.getState().selectedNote.title;
    store.dispatch(updateNote(res.note));
    if (oldTitle !== res.note.title) noteList(store);
  }).fail((err) => {
    console.log('failure');
  });
}

export function deleteNoteRequest(store) {
  const id = store.getState().selectedNote.id;
  const aTkn = store.getState().accessToken;
  $.ajax({
    url: `http://localhost:9000/api/v1.0/notes/${id}`,
    crossDomain: true,
    type: 'DELETE',
    headers: { Authorization: `Bearer ${aTkn}` },
  }).done(() => {
    store.dispatch(deleteNote(id));
    store.dispatch(selectNote(null));
    noteList(store);
    newNoteForm(store);
  }).fail((err) => {
    console.log(err);
  });
}
