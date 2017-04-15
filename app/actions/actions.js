import * as types from './actionTypes';


export function addNote(note) {
  return { type: types.ADD_NOTE, note };
}

export function deleteNote(id) {
  return { type: types.DELETE_NOTE, id };
}

export function updateNote(note) {
  return { type: types.UPDATE_NOTE, note };
}

export function getNotes() {
  return { type: types.GET_NOTES };
}

export function selectNote(id) {
  return { type: types.SELECT_NOTE, id };
}

export function login(userEmail, accessToken) {
  return { type: types.LOGIN, userEmail, accessToken };
}

export function logout() {
  return { type: types.LOGOUT };
}

export function getAccessToken(userEmail, accessToken) {
  return { type: types.GET_ACCESS_TOKEN, userEmail, accessToken };
}

export function authFail(userEmail, errMsg) {
  return { type: types.AUTH_FAIL, userEmail, errMsg };
}
