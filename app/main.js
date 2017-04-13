/* eslint-env browser, jquery */

import {
  navbar,
  loginForm,
  registerForm,
} from './renders';
import {
  login,
  logout,
  register,
  getAccessToken,
} from './auth';
import { getNotes } from './notes';

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

    if(ev.target.id === 'logout') {
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
  });
});
