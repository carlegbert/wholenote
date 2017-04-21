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
  noteDetail,
  noteList,
} from './renders';

import { accessTokenRequest, loginRequest } from './auth';

export function getNoteRequest(store) {
  const aTkn = store.getState().accessToken;
  $.ajax({
    url: '/api/v1.0/notes',
    type: 'GET',
    headers: { Authorization: `Bearer ${aTkn}` },
  }).done((res) => {
    store.dispatch(getNotes(res.notes));
    allNoteElements(store);
  }).fail((err) => {
    if (err.status === 401 && err.responseJSON.msg === 'Token has expired') {
      accessTokenRequest(store, [getNoteRequest], [loginRequest]);
    }
  });
}

export function createNoteRequest(store) {
  const aTkn = store.getState().accessToken;
  const title = $('#new-title').val() || 'new note';
  const text = $('#new-text').val();
  const data = JSON.stringify({ title, text });

  $.ajax({
    url: '/api/v1.0/notes',
    type: 'POST',
    headers: { Authorization: `Bearer ${aTkn}` },
    contentType: 'application/json',
    data,
  }).done((res) => {
    store.dispatch(addNote(res.note));
    store.dispatch(selectNote(res.note.id));
    noteList(store);
    noteDetail(store);
    $('.selected-note-li').removeClass('selected-note-li');
    $(`#${res.note.id}`).addClass('selected-note-li');
  }).fail((err) => {
    if (err.status === 401 && err.responseJSON.msg === 'Token has expired') {
      accessTokenRequest(store, [createNoteRequest], [loginRequest]);
    }
  });
}

export function updateNoteRequest(store) {
  const title = $('#update-title').val() || 'untitled note';
  const text = $('#update-text').val();
  const data = JSON.stringify({ title, text });
  const aTkn = store.getState().accessToken;
  const id = store.getState().selectedNote.id;
  $.ajax({
    url: `/api/v1.0/notes/${id}`,
    type: 'PUT',
    headers: { Authorization: `Bearer ${aTkn}` },
    contentType: 'application/json',
    data,
  }).done((res) => {
    const oldTitle = store.getState().selectedNote.title;
    store.dispatch(updateNote(res.note));
    if (oldTitle !== res.note.title) {
      $(`#${id}`).html(res.note.title);
    }
  }).fail((err) => {
    if (err.status === 401 && err.responseJSON.msg === 'Token has expired') {
      accessTokenRequest(store, [updateNoteRequest], [loginRequest]);
    }
  });
}

export function deleteNoteRequest(store) {
  const id = store.getState().selectedNote.id;
  const aTkn = store.getState().accessToken;
  $.ajax({
    url: `/api/v1.0/notes/${id}`,
    type: 'DELETE',
    headers: { Authorization: `Bearer ${aTkn}` },
  }).done(() => {
    store.dispatch(deleteNote(id));
    store.dispatch(selectNote(null));
    noteList(store);
    newNoteForm(store);
  }).fail((err) => {
    if (err.status === 401 && err.responseJSON.msg === 'Token has expired') {
      accessTokenRequest(store, [deleteNoteRequest], loginRequest);
    }
  });
}
