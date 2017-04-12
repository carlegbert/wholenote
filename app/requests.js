/* eslint-env browser, jquery */

import {
  loginForm,
  registerForm,
  noteList,
} from './renders';

export function login() {
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
    console.log('login successful');
    localStorage.setItem('refreshToken', res.refresh_token);
    sessionStorage.setItem('accessToken', res.access_token);
    noteList();
  }).fail((err) => {
    loginForm(err.responseJSON.error, email);
  });
}

export function register() {
  const pw = $('#reg-pw').val();
  const email = $('#reg-email').val();
  const data = JSON.stringify({ email: email, password: pw });
  $.ajax({
    url: 'http://localhost:9000/api/v1.0/register',
    crossDomain: true,
    type: 'POST',
    contentType: 'application/json',
    data: data,
  }).done((res) => {
    console.log('register successful');
  }).fail((err) => {
    registerForm(err.responseJSON.error, email);
  });
}

export function getAccessToken(successCallback, failCallback) {
  // use refresh token to retrieve access token from server
  // Because refresh requests can be sent during different circumstances
  // (on page load or after expiring), different render actions
  // are needed depending on the current page state. Callback functions
  // are passed in depending on what we want to happen on succesful or
  // unsuccesful refresh requests.
  const rTkn = localStorage.getItem('refreshToken');
  $.ajax({
    url: 'http://localhost:9000/api/v1.0/refresh',
    crossDomain: true,
    type: 'POST',
    headers: { Authorization: `Bearer ${rTkn}` },
  }).done((res) => {
    successCallback();
    sessionStorage.setItem('accessToken', res.access_token);
  }).fail((err) => {
    console.log('refresh fail');
    console.log(err);
    failCallback();
  });

}
