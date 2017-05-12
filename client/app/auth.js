/* eslint-env browser, jquery */

import {
  login,
  logout,
  saveAccessToken,
  authFail,
} from './actions/actions';

import {
  renderLoginForm,
  renderNavbar,
  renderRegisterForm,
} from './renders';
import { getNoteRequest } from './notes';

export function loginRequest(store) {
  const pw = $('#login-pw').val();
  const email = $('#login-email').val();
  const enc = window.btoa(`${email}:${pw}`);
  $.ajax({
    url: '/api/v1.0/login',
    type: 'POST',
    headers: {
      Authorization: `Basic ${enc}`,
    },
  }).done((res) => {
    localStorage.setItem('refreshToken', res.refresh_token);
    store.dispatch(login(email, res.access_token));
    sessionStorage.setItem('accessToken', res.access_token);
    renderNavbar(store);
    getNoteRequest(store);
  }).fail((err) => {
    const errMsg = err.responseJSON.msg;
    store.dispatch(authFail(email));
    renderLoginForm(store, errMsg);
  });
}

export function registerRequest(store) {
  const email = $('#reg-email').val();
  const password = $('#reg-pw').val();
  const confirm = $('#reg-confirm').val();
  if (password !== confirm) {
    store.dispatch(authFail(email));
    renderRegisterForm(store, "Passwords don't match");
    return;
  }
  const data = JSON.stringify({ email, password });
  $.ajax({
    url: '/api/v1.0/register',
    type: 'POST',
    contentType: 'application/json',
    data,
  }).done((res) => {
    if (res.message.includes('verified')) {
      $('#main').html(`
        <div class="col-xs-6 col-xs-offset-3 reg-success text-center">
          <h3>Registration for ${email} successful.
          Please check your email to verify your account.</h3>
        </div>
      `);
    } else {
      // In case of an error in sending mail, the server will
      // automatically verify the user's email and send an access token.
      localStorage.setItem('refreshToken', res.refresh_token);
      store.dispatch(login(email, res.access_token));
      sessionStorage.setItem('accessToken', res.access_token);
      renderNavbar(store);
      getNoteRequest(store);
    }
    localStorage.setItem('refreshToken', res.refresh_token);
  }).fail((err) => {
    const errMsg = err.responseJSON.msg;
    store.dispatch(authFail(email));
    renderRegisterForm(store, errMsg);
  });
}

export function logoutRequest(store) {
  store.dispatch(logout());
  localStorage.setItem('refreshToken', '');
  sessionStorage.setItem('accessToken', '');
  localStorage.setItem('currentUser', '');
  renderNavbar(store);
  renderLoginForm(store);
}

export function accessTokenRequest(store, successCallbacks = [], failCallbacks = []) {
  // Use refresh token to retrieve access token from server.
  // Because refresh requests can be sent during different circumstances
  // (on page load or after a token expiring), different render actions
  // are needed depending on the current page state. Callback functions
  // are passed in depending on what we want to happen on succesful or
  // unsuccesful refresh requests. Redux store is passed to callback functions.
  // successCallbacks and failCallbacks should both be arrays of functions.
  const rTkn = localStorage.getItem('refreshToken');
  $.ajax({
    url: '/api/v1.0/refresh',
    type: 'POST',
    headers: { Authorization: `Bearer ${rTkn}` },
  }).done((res) => {
    store.dispatch(saveAccessToken(res.email, res.access_token));
    successCallbacks.forEach(callback => callback(store));
    sessionStorage.setItem('accessToken', res.access_token);
  }).fail(() => {
    failCallbacks.forEach(callback => callback(store));
    // clear old access token on failure
    sessionStorage.setItem('accessToken', '');
    store.dispatch(saveAccessToken(null, null));
  });
}
