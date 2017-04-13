/* eslint-env browser, jquery */

import {
  loginForm,
  navbar,
  registerForm,
} from './renders';
import { getNotes } from './notes';

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
    localStorage.setItem('refreshToken', res.refresh_token);
    localStorage.setItem('currentUser', email);
    sessionStorage.setItem('accessToken', res.access_token);
    navbar();
    getNotes(res.access_token);
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
  }).done(() => {
    $('#main').html(`
      <div class="jumbotron">
        <h3 class="text-center">Registration for ${email} successful.
        Please check your email to verify your account.</h3>
      </div>
    `);
  }).fail((err) => {
    registerForm(err.responseJSON.error, email);
  });
}

export function logout() {
  localStorage.setItem('refreshToken', '');
  sessionStorage.setItem('accessToken', '');
  localStorage.setItem('currentUser', '');
  navbar();
  loginForm();
}

export function getAccessToken(successCallback, failCallback) {
  // Use refresh token to retrieve access token from server.
  // Because refresh requests can be sent during different circumstances
  // (on page load or after a token expiring), different render actions
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
    successCallback(res.access_token);
    sessionStorage.setItem('accessToken', res.access_token);
  }).fail(() => {
    failCallback();
  });
}
