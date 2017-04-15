/* eslint-env browser, jquery */
import { createStore } from 'redux';

import notesApp from './reducers';

import {
  navbar,
  newNoteForm,
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
  createNote,
  getNotes,
} from './notes';

require('./styles.css');

$(document).ready(() => {
  navbar();

  let store = createStore(notesApp);

  if (store.getState().accessToken) {
    getAccessTokenRequest(store, getNotes, loginForm);
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
      createNote(store);
    }
  });
});
