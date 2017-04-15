import * as types from './actions/actionTypes';

const initialState = {
  userEmail: null,
  accessToken: null,
  notes: [],
  selectedNote: null,
};

function notesApp(state = initialState, action) {
  switch (action.type) {
    case types.LOGIN:
      return Object.assign({}, state, {
        userEmail: action.userEmail,
        accessToken: action.accessToken,
      });
    case types.LOGOUT:
      return Object.assign({}, state, {
        userEmail: null,
        accessToken: null,
        notes: [],
        selectedNote: null,
      });
    case types.GET_ACCESS_TOKEN:
      return Object.assign({}, state, {
        accessToken: action.accessToken,
        userEmail: action.userEmail,
      });
    case types.AUTH_FAIL:
      return Object.assign({}, state, {
        userEmail: action.userEmail,
        errMsg: action.errMsg,
      });
    case types.GET_NOTES:
      return Object.assign({}, state, {
        notes: action.notes,
      });
    case types.ADD_NOTE:
      return Object.assign({}, state, {
        notes: [...state.notes, action.newNote],
      });

    default:
      return state;
  }
}

export default notesApp;
