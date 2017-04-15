/* eslint-env browser, jquery */

export function navbar(store) {
  const email = localStorage.getItem('currentUser');
  let navContent;
  if (!email) {
    navContent = '<li id="log-or-reg"></li>';
  } else {
    navContent = `
    <ul class="nav navbar-right">
      <li>logged in as ${email}</li>
      <li><a id="account-info">account</a></li>
      <li><a id="logout">log out</a></li>
    </ul>`;
  }

  $('#navbar-header').html(
    `<nav class="navbar navbar-default">
      <div class="container-fluid">
        <div class="navbar-header">
          <a class="navbar-brand" href="/">wholenote</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-right" id="nav-content">${navContent}</ul>
        </div>
      </div>
    </nav>`);
}

export function loginForm(store) {
  const email = store.getState().userEmail || '';
  const errMsg = store.getState().errMsg || '';
  $('#main').html(`
    <div class="err-msg"><h3>${errMsg}</h3><div>
    <form id="login-form">
      <input placeholder="email" type="email" id="login-email" value=${email} >
      <input placeholder="password" id="login-pw" type="password" >
      <button id="login-submit">Log in</button>
    </form>
  `);

  $('#log-or-reg').html('<a id="register">register</a>');
}

export function registerForm(store) {
  const email = store.getState().userEmail || '';
  const errMsg = store.getState().errMsg || '';
  $('#main').html(`
    <div class="err-msg"><h3>${errMsg}</h3><div>
    <form id="reg">
      <input placeholder="email" type="email" id="reg-email" value=${email} >
      <input placeholder="password" id="reg-pw" type="password" >
      <input placeholder="confirm password" id="reg-conf" type="password" >
      <button id="reg-submit">Register</button>
    </form>
  `);

  $('#log-or-reg').html('<a id="login">login</a>');
}

export function noteList(store) {
  const notes = store.getState().notes;
  $('#main').html(`
    <div class="container">
      <div class="col-xs-3 text-center" id="note-list">
        <div class="panel panel-default new-note">
          <h4 class="new-note">+ new note</h4>
        </div>
      </div>
      <div class="col-xs-9" id="note-detail"></div>
    </div>
  `);

  notes.forEach((note) => {
    $('#note-list').append(`
      <div class="panel panel-default" id="${note.id}">
        <h4>${note.title}</h4>
      </div>
    `);
  });
}

export function newNoteForm() {
  $('#note-detail').html(`
    <div class="note-detail-container">
      <div class="note-title-container">
        <textarea id="new-title" placeholder="title" />
        <button id="new-note-submit" class="btn btn-submit">save</button>
      </div>
      <textarea id="new-text" placeholder="text" />
    </div>
  `);
}
