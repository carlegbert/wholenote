/* eslint-env browser, jquery */

import {
  addNote,
  getNotes,
  deleteNote,
  updateNote,
} from './actions/actions';

import {
  renderAllNoteElements,
  renderNoteActionFeedback,
  renderNoteDetail,
  renderNoteList,
} from './renders';

import { accessTokenRequest } from './auth';

export function getNoteRequest(store) {
  const aTkn = store.getState().accessToken;
  $.ajax({
    url: '/api/v1.0/notes',
    type: 'GET',
    headers: { Authorization: `Bearer ${aTkn}` },
  }).done((res) => {
    store.dispatch(getNotes(res.notes));
    renderAllNoteElements(store);
  }).fail((err) => {
    if (err.status === 401 && err.responseJSON.msg === 'Token has expired') {
      accessTokenRequest(store, [getNoteRequest]);
    }
  });
}

export function createNoteRequest(store) {
  const aTkn = store.getState().accessToken;
  const title = 'new note';
  const text = '';
  const data = JSON.stringify({ title, text });

  $.ajax({
    url: '/api/v1.0/notes',
    type: 'POST',
    headers: { Authorization: `Bearer ${aTkn}` },
    contentType: 'application/json',
    data,
  }).done((res) => {
    store.dispatch(addNote(res.note));
    renderNoteList(store);
    renderNoteDetail(store);
    const titleElement = $('#update-title')[0];
    titleElement.focus();
    titleElement.setSelectionRange(0, 8);
    $('.selected-note-li').removeClass('selected-note-li');
    $(`#${res.note.id}`).addClass('selected-note-li');
  }).fail((err) => {
    if (err.status === 401 && err.responseJSON.msg === 'Token has expired') {
      accessTokenRequest(store, [createNoteRequest]);
    }
  });
}

export function updateNoteRequest(store) {
  const selectedNote = store.getState().selectedNote;
  if (!selectedNote) return;
  const title = $('#update-title').val() || 'untitled note';
  const text = $('#update-text').val();
  const oldTitle = selectedNote.title;
  const oldText = selectedNote.text;
  if ((oldTitle === title) && oldText === text) return;

  const data = JSON.stringify({ title, text });
  const aTkn = store.getState().accessToken;
  $.ajax({
    url: `/api/v1.0/notes/${selectedNote.titleId}`,
    type: 'PUT',
    headers: { Authorization: `Bearer ${aTkn}` },
    contentType: 'application/json',
    data,
  }).done((res) => {
    renderNoteActionFeedback(`${title} has been saved`);
    store.dispatch(updateNote(res.note));
    if (oldTitle !== res.note.title) {
      $(`#${note.id}`).html(res.note.title);
    }
  }).fail((err) => {
    if (err.status === 401 && err.responseJSON.msg === 'Token has expired') {
      accessTokenRequest(store, [updateNoteRequest]);
    }
  });
}

export function deleteNoteRequest(store) {
  const note = store.getState().selectedNote;
  const aTkn = store.getState().accessToken;
  $.ajax({
    url: `/api/v1.0/notes/${note.titleId}`,
    type: 'DELETE',
    headers: { Authorization: `Bearer ${aTkn}` },
  }).done(() => {
    renderNoteActionFeedback(`${store.getState().selectedNote.title} has been deleted`);
    store.dispatch(deleteNote(note.id));
    $(`#${note.id}`).remove();
    renderNoteDetail(store);
  }).fail((err) => {
    if (err.status === 401 && err.responseJSON.msg === 'Token has expired') {
      accessTokenRequest(store, [deleteNoteRequest]);
    }
  });
}
