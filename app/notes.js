/* eslint-env browser, jquery */

import {
  noteList,
} from './renders';


export function getNotes(aTkn) {
  $.ajax({
    url: 'http://localhost:9000/api/v1.0/notes',
    crossDomain: true,
    type: 'GET',
    headers: { Authorization: `Bearer ${aTkn}` },
  }).done((res) => {
    noteList(res.notes);
  });
}

export function createNote() {
  const aTkn = sessionStorage.getItem('accessToken');
  const title = $('#new-title').val();
  const text = $('#new-text').val();
  const data = JSON.stringify({ title: title, text: text });

  $.ajax({ url: 'http://localhost:9000/api/v1.0/notes',
    crossDomain: true,
    type: 'POST',
    headers: { Authorization: `Bearer ${aTkn}` },
    contentType: 'application/json',
    data: data,
  }).done((res) => {
    console.log('success');
  }).fail((err) => {
    console.log('failure');
  })
}
