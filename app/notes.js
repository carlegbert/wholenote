import {
  noteList,
} from './renders';


export function getNotes() {
  const aTkn = sessionStorage.getItem('accessToken');
  $.ajax({
    url: 'http://localhost:9000/api/v1.0/notes',
    crossDomain: true,
    type: 'GET',
    headers: { Authorization: `Bearer ${aTkn}` },
  }).done((res) => {
    noteList(res.notes);
  });
}
