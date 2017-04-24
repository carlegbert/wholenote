/* eslint-env browser, jquery */

export function renderNavbar(store) {
  const email = store.getState().userEmail;
  let navContent;
  if (!email) {
    navContent = '<span id="log-or-reg"></span>';
  } else {
    navContent = `
      logged in as ${email} /
      <a class="navlink" id="logout">log out</a>`;
  }

  $('#navbar-header').html(`
    <div class=col-xs-12>
      <div class="navbar-header col-xs-2">
        <a href="/">wholenote</a>
      </div>
      <div class="text-right">
        <div class="nav navbar-nav navbar-right">
          ${navContent} /
          <a href="#" id="about">about</a>
        </div>
      </div>
    </div>
  `);
}

export function renderLoginForm(store, errMsg = '') {
  const email = store.getState().userEmail || '';
  $('#main').html(`
    <div class="col-sm-6 col-sm-offset-3 text-center">
      <div class="err-msg"><h3>${errMsg}</h3><div>
      <form id="login-form">
        <input placeholder="email" type="email" id="login-email" value=${email} >
        <input placeholder="password" id="login-pw" type="password" >
        <button class="auth-btn btn btn-success" id="login-submit">Log in</button>
      </form>
    </div>
  `);

  $('#log-or-reg').html('<a href="#" id="register">register</a>');
}

export function renderRegisterForm(store, errMsg = '') {
  const email = store.getState().userEmail || '';
  $('#main').html(`
    <div class="col-sm-6 col-sm-offset-3 text-center">
      <div class="err-msg"><h3>${errMsg}</h3><div>
      <form id="reg">
        <input placeholder="email" type="email" id="reg-email" value=${email} >
        <input placeholder="password" id="reg-pw" type="password" >
        <input placeholder="confirm password" id="reg-confirm" type="password" >
        <button class="auth-btn btn btn-success" id="reg-submit">Register</button>
      </form>
    </div>
  `);

  $('#log-or-reg').html('<a href="#" id="login">login</a>');
}

export function renderNoteList(store) {
  const notes = store.getState().notes;
  $('#note-list').html('');
  notes.forEach((note) => {
    $('#note-list').prepend(`
      <div class="panel panel-default note-li note-detail-link" id="${note.id}">
        ${note.title}
      </div>
    `);
  });
}

export function renderNewNoteForm() {
  $('.selected-note-li').removeClass('selected-note-li');
  $('#new-note-button').addClass('selected-note-li');

  $('#note-detail').html(`
    <div class="note-detail-container">
      <div class="note-title-container">
        <textarea id="new-title" placeholder="new note" />
      </div>
      <textarea id="new-text" placeholder="text" />
      <div class="button-container text-center">
        <button id="new-note-submit" class="btn btn-success">save</button>
      </div>
    </div>
  `);
}

export function renderNoteDetail(store) {
  $('.selected-note-li').removeClass('selected-note-li');
  if (store.getState().notes.length === 0) {
    $('#note-detail').html(`
      <div class="text-center new-note-exp">
        <h3>
          looks like you haven't created any notes yet.
          <a class="new-note-button" href="#">click</a> to create one.
        </h3>
      </div>`);
    return;
  }

  $(`#${store.getState().selectedNote.id}`).addClass('selected-note-li');
  const title = store.getState().selectedNote.title;
  const text = store.getState().selectedNote.text;
  $('#note-detail').html(`
    <div class="note-detail-container">
      <div class="note-title-container">
        <textarea id="update-title" placeholder="title">${title}</textarea>
      </div>
      <textarea id="update-text" placeholder="text">${text}</textarea>
      <div class="button-container text-center">
        <button id="update-note-submit" class="btn btn-success">save</button>
        <button class="btn btn-danger" id="delete-note">delete</button>
      </div>
    </div>
  `);
}

export function renderNoteActionFeedback(notification = '') {
  $('#note-feedback-container').html(`<div id="note-feedback">${notification}</div>`);
  setTimeout(() => $('#note-feedback').fadeOut(), 8000);
}

export function renderAllNoteElements(store) {
  $('#main').html(`
    <div class="container">
      <div class="col-xs-3 text-center">
        <div class="panel panel-default new-note-button" id="new-note-button">
          + new note
        </div>
        <div id="note-list"></div>
      </div>
      <div class="col-xs-9">
        <div id="note-feedback-container" class="text-center"></div>
        <div id="note-detail"></div>
      </div>
    </div>
  `);

  renderNoteList(store);
  renderNoteDetail(store);
}
