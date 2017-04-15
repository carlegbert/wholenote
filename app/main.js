/* eslint-env browser, jquery */
import { createStore } from 'redux';

import notesApp from './reducers';

import { selectNote } from './actions/actions';

import {
  navbar,
  newNoteForm,
  noteDetail,
  loginForm,
  registerForm,
} from './renders';
import {
  loginRequest,
  logoutRequest,
  registerRequest,
  getAccessTokenRequest,
} from './auth';
import {
  createNoteRequest,
  getNoteRequest,
  updateNoteRequest,
} from './notes';

require('./styles.css');

$(document).ready(() => {
  navbar();

  const store = createStore(notesApp);

  if (localStorage.getItem('refreshToken')) {
    getAccessTokenRequest(store, getNoteRequest, loginForm);
  } else {
    loginForm(store);
  }

  document.addEventListener('click', (ev) => {
    if (ev.target.id === 'register') {
      registerForm(store);
    }

    if (ev.target.id === 'login') {
      loginForm(store);
    }

    if (ev.target.id === 'logout') {
      logoutRequest(store);
    }

    if (ev.target.id === 'login-submit') {
      ev.preventDefault();
      loginRequest(store);
    }

    if (ev.target.id === 'reg-submit') {
      ev.preventDefault();
      registerRequest(store);
    }

    if (ev.target.classList.contains('new-note')) {
      newNoteForm();
    }

    if (ev.target.id === 'new-note-submit') {
      createNoteRequest(store);
    }

    if (ev.target.classList.contains('note-detail')) {
      store.dispatch(selectNote(event.target.id));
      noteDetail(store);
    }

    if (ev.target.id === 'update-note-submit') {
      updateNoteRequest(store);
    }
  });
});
