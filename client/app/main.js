/* eslint-env browser, jquery */
import { createStore } from 'redux';

import notesApp from './reducers';

import { selectNote } from './actions/actions';

import {
  about,
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
    accessTokenRequest(store, [getNoteRequest, navbar], [loginForm, navbar]);
  } else {
    navbar(store);
    loginForm(store);
  }

  document.addEventListener('click', (ev) => {
    if (ev.target.id === 'about' || event.target.id === 'close-about') {
      $('#about-page').toggle();
      $('#main').toggle();
      $('#about-link').toggle();
      $('#back-link').toggle();
    }

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

    if (ev.target.id === 'new-note') {
      $('.selected-note-li').removeClass('selected-note-li');
      $(`#new-note`).addClass('selected-note-li');
      newNoteForm();
    }

    if (ev.target.id === 'new-note-submit') {
      createNoteRequest(store);
    }

    if (ev.target.classList.contains('note-detail-link')) {
      store.dispatch(selectNote(event.target.id));
      $('.selected-note-li').removeClass('selected-note-li');
      $(`#${event.target.id}`).addClass('selected-note-li');
      noteDetail(store);
    }

    if (ev.target.id === 'update-note-submit') {
      updateNoteRequest(store);
    }

    if (ev.target.id === 'delete-note') {
      deleteNoteRequest(store);
    }
  });
});
