/* eslint-env browser, jquery */

import {
  addNote,
  getNotes,
} from './actions/actions';

import {
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
    noteList(store);
  });
}

export function createNoteRequest(store) {
  const aTkn = store.getState().accessToken;
  const title = $('#new-title').val();
  const text = $('#new-text').val();
  const data = JSON.stringify({ title, text });

  $.ajax({ url: 'http://localhost:9000/api/v1.0/notes',
    crossDomain: true,
    type: 'POST',
    headers: { Authorization: `Bearer ${aTkn}` },
    contentType: 'application/json',
    data,
  }).done((res) => {
    console.log(res.note.id);
    store.dispatch(addNote(res.note));
    noteList(store);
  }).fail((err) => {
    console.log('failure');
  });
}
