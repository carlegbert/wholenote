/* eslint-env browser, jquery */

import {
  login,
  logout,
  getAccessToken,
  authFail,
} from './actions/actions';

import {
  loginForm,
  navbar,
  registerForm,
} from './renders';
import { getNoteRequest } from './notes';

export function loginRequest(store) {
  const pw = $('#login-pw').val();
  const email = $('#login-email').val();
  const enc = window.btoa(`${email}:${pw}`);
  $.ajax({
    url: 'http://localhost:9000/api/v1.0/login',
    crossDomain: true,
    type: 'POST',
    headers: {
      Authorization: `Basic ${enc}`,
    },
  }).done((res) => {
    localStorage.setItem('refreshToken', res.refresh_token);
    store.dispatch(login(email, res.access_token));
    localStorage.setItem('currentUser', email);
    sessionStorage.setItem('accessToken', res.access_token);
    navbar(store);
    getNoteRequest(store);
  }).fail((err) => {
    const errMsg = err.responseJSON.error || err.responseJSON.msg;
    store.dispatch(authFail(email, errMsg));
    loginForm(store);
  });
}

export function registerRequest(store) {
  const email = $('#reg-email').val();
  const password = $('#reg-pw').val();
  const confirm = $('#reg-confirm').val();
  if (password !== confirm) {
    store.dispatch(authFail(email, "Passwords don't match"));
    registerForm(store);
    return;
  }
  const data = JSON.stringify({ email, password });
  $.ajax({
    url: 'http://localhost:9000/api/v1.0/register',
    crossDomain: true,
    type: 'POST',
    contentType: 'application/json',
    data,
  }).done(() => {
    $('#main').html(`
      <div class="col-xs-6 col-xs-offset-3 reg-success text-center">
        <h3>Registration for ${email} successful.
        Please check your email to verify your account.</h3>
      </div>
    `);
  }).fail((err) => {
    const errMsg = err.responseJSON.error || err.responseJSON.msg;
    store.dispatch(authFail(email, errMsg));
    registerForm(store);
  });
}

export function logoutRequest(store) {
  store.dispatch(logout());
  localStorage.setItem('refreshToken', '');
  sessionStorage.setItem('accessToken', '');
  localStorage.setItem('currentUser', '');
  navbar(store);
  loginForm(store);
}

export function accessTokenRequest(store, successCallbacks, failCallback) {
  // Use refresh token to retrieve access token from server.
  // Because refresh requests can be sent during different circumstances
  // (on page load or after a token expiring), different render actions
  // are needed depending on the current page state. Callback functions
  // are passed in depending on what we want to happen on succesful or
  // unsuccesful refresh requests. Redux store is passed to callback functions.
  // successCallbacks is an array of functions; failCallback is a single function.
  const rTkn = localStorage.getItem('refreshToken');
  $.ajax({
    url: 'http://localhost:9000/api/v1.0/refresh',
    crossDomain: true,
    type: 'POST',
    headers: { Authorization: `Bearer ${rTkn}` },
  }).done((res) => {
    store.dispatch(getAccessToken(res.email, res.access_token));
    successCallbacks.forEach(callback => callback(store));
    localStorage.setItem('accessToken', res.access_token);
  }).fail(() => {
    failCallback(store);
  });
}
