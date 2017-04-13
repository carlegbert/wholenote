/* eslint-env browser, jquery */

import {
  navbar,
  newNoteForm,
  loginForm,
  registerForm,
} from './renders';
import {
  login,
  logout,
  register,
  getAccessToken,
} from './auth';
import {
  createNote,
  getNotes,
} from './notes';

require('./styles.css');

$(document).ready(() => {
  navbar();

  const sessionObject = {
    aTkn: sessionStorage.getItem('accessToken'),
  };

  if (sessionObject.aTkn) {
    getAccessToken(getNotes, loginForm);
  } else {
    loginForm();
  }

  document.addEventListener('click', (ev) => {
    if (ev.target.id === 'register') {
      registerForm();
    }

    if (ev.target.id === 'login') {
      loginForm();
    }

    if (ev.target.id === 'logout') {
      logout();
    }

    if (ev.target.id === 'login-submit') {
      ev.preventDefault();
      login();
    }

    if (ev.target.id === 'reg-submit') {
      ev.preventDefault();
      register();
    }

    if (ev.target.classList.contains('new-note')) {
      newNoteForm();
    }

    if (ev.target.id === 'new-note-submit') {
      createNote();
    }
  });
});
