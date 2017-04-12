/* eslint-env browser, jquery */

import {
  navbar,
  loginForm,
  registerForm,
} from './renders';

$(document).ready(() => {
  navbar();
  loginForm();

  document.addEventListener('click', (ev) => {
    if (ev.target.id === 'register') {
      registerForm();
    }

    if (ev.target.id === 'login') {
      loginForm();
    }

    if (ev.target.id === 'login-submit') {
      ev.preventDefault();
    }
  });
});
