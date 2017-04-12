/* eslint-env browser, jquery */

import {
  navbar,
  loginForm,
  registerForm,
  noteList,
} from './renders';
import {
  login,
  register,
  getAccessToken,
} from './requests';

$(document).ready(() => {
  navbar();

  const sessionObject = {
    aTkn: sessionStorage.getItem('accessToken'),
  };

  if (sessionObject.aTkn) {
    getAccessToken(noteList, loginForm);
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

    if (ev.target.id === 'login-submit') {
      ev.preventDefault();
      login();
    }

    if (ev.target.id === 'reg-submit') {
      ev.preventDefault();
      register();
    }
  });
});
