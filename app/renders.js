/* eslint-env jquery */

export function navbar(user = '') {
  let navContent;
  if (!user) {
    navContent = '<li id="log-or-reg"></li>';
  } else {
    navContent = `
    <ul class="nav navbar-right">
      <li>logged in as {user}</li>
      <li><a id="account-info">account</a></li>
      <li><a id="logout">log out</a></li>
    </ul>
    `;
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

export function loginForm(err = '', email = '') {
  $('#main').html(`
    <div class="err-msg" id="login-err">${err}</div>
    <form id="login-form">
      <input placeholder="email" type="email" id="login-email" value=${email} >
      <input placeholder="password" type="login-pw" type="password" >
      <button id="login-submit">Log in</button>
    </form>
  `);

  $('#log-or-reg').html('<a id="register">register</a>');
}

export function registerForm(err = '', email = '') {
  $('#main').html(`
    <div class="reg-msg" id="reg-err">${err}</div>
    <form id="reg">
      <input placeholder="email" type="email" id="reg-email" value=${email} >
      <input placeholder="password" type="reg-pw" type="password" >
      <input placeholder="confirm password" type="reg-conf" type="password" >
      <button id="reg-submit">Register</button>
    </form>
  `);

  $('#log-or-reg').html('<a id="login">login</a>');
}
