/* eslint-env browser, jquery */
import { createStore } from 'redux';

import notesApp from './reducers';

import { selectNote } from './actions/actions';
import {
  renderNavbar,
  renderNoteDetail,
  renderLoginForm,
  renderRegisterForm,
} from './renders';
import {
  loginRequest,
  logoutRequest,
  registerRequest,
  accessTokenRequest,
} from './auth';
import {
  createNoteRequest,
  getNoteRequest,
  deleteNoteRequest,
  updateNoteRequest,
} from './notes';

require('./styles.css');

$(document).ready(() => {
  const store = createStore(notesApp);

  if (localStorage.getItem('refreshToken')) {
    accessTokenRequest(store, [renderNavbar, getNoteRequest], [renderNavbar, renderLoginForm]);
  } else {
    renderNavbar(store);
    renderRegisterForm(store);
  }

  document.addEventListener('click', (ev) => {
    if (ev.target.id === 'about' || ev.target.id === 'close-about') {
      $('#about-page').toggle();
      $('#main').toggle();
      $('#about-link').toggle();
      $('#back-link').toggle();
    }

    if (ev.target.classList.contains('register')) {
      renderRegisterForm(store);
    }

    if (ev.target.classList.contains('login')) {
      renderLoginForm(store);
    }

    if (ev.target.id === 'logout') {
      updateNoteRequest(store);
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

    if (ev.target.classList.contains('new-note-button')) {
      updateNoteRequest(store);
      createNoteRequest(store);
    }

    if (ev.target.classList.contains('note-detail-link')) {
      updateNoteRequest(store);
      store.dispatch(selectNote(ev.target.id));
      renderNoteDetail(store);
      const element = $('#update-text')[0];
      const len = store.getState().selectedNote.text.length;
      element.focus();
      element.setSelectionRange(len, len);
    }

    if (ev.target.id === 'update-note-submit') {
      updateNoteRequest(store);
    }

    if (ev.target.id === 'delete-note') {
      deleteNoteRequest(store);
    }
  });
});
