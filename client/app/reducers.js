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
        errMsg: null,
      });
    case types.LOGOUT:
      return Object.assign({}, state, {
        userEmail: null,
        accessToken: null,
        notes: [],
        selectedNote: null,
        errMsg: null,
      });
    case types.SAVE_ACCESS_TOKEN:
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
    case types.SELECT_NOTE:
      return Object.assign({}, state, {
        selectedNote: state.notes.filter(note => note.id === action.id)[0],
      });
    case types.UPDATE_NOTE:
      return Object.assign({}, state, {
        notes: [
          ...state.notes.filter(note => note.id !== action.updatedNote.id),
          action.updatedNote,
        ],
      });
    case types.DELETE_NOTE:
      return Object.assign({}, state, {
        notes: state.notes.filter(note => note.id !== action.id),
      });
    default:
      return state;
  }
}

export default notesApp;
