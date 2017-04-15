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
  createNoteRequest,
  getNoteRequest,
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
  });
});
