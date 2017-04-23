# API endpoints

## Errors

All endpoints return JSON including descriptive error messages and appropriate status codes, usually formatted like so:
```
{
  'error': 'Login failed (incorrect email or password)',
  'statusCode': 403
}
```

Some authentication errors (those involving bearer tokens) will return JSON with a 'msg' property rather than 'error'.

## Authentication

### /api/v1.0/login - POST

#### Accepts:

A POST request with HTTP Basic Authorization. The username and password should be base64 encoded.

Example AJAX request:
```
const email = 'john@doe.com';
const pw = 'hunter2';
const encodedInfo = window.btoa(email+":"+pw);
$.ajax({
  url: <url>,
  crossDomain: true,
  type: 'POST',
  headers: { Authorization: 'Basic '+encodedInfo },
})...
```

#### Returns:

A JSON response including a message, an access token, and a refresh token.

Example response JSON:
```
{
  "message": "Login for john@doe succesful",
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>",
  "statusCode": 200
}
```

### /api/v1.0/register - POST

#### Accepts:

A POST request with data passed as JSON. A register request does return access tokens, but users are required to verify their email address before using their account.

Example AJAX request:
```
const email = 'john@doe.com';
const pw = 'hunter2';
const encodedInfo = window.btoa(email+":"+pw);
$.ajax({
  url: <url>,
  crossDomain: true,
  type: 'POST',
  contentType: 'application/JSON',
  data: {
    email: email,
    password: pw
  }
})...
```

#### Returns:

A JSON response including a message, an access token, and a refresh token.

Example response JSON:
```
{
  "message": "Account registered for john@doe",
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>",
  "statusCode": 200
}
```

### /api/v1.0/refresh - POST

#### Accepts:

A POST request with a refresh token passed as an authorization header.

Example AJAX request:
```
const encodedInfo = window.btoa(email+":"+pw);
$.ajax({
  url: <url>,
  crossDomain: true,
  type: 'POST',
  headers: { Authorization: 'Bearer ' + <refresh token> },
})...
```

#### Returns:

A JSON response including a message, an access token, and the user's email address.

Example response JSON:
```
{
  "message": "Success",
  "access_token": "<access_token>",
  "email" "john@doe",
  "statusCode": 200
}
```

## Note CRUD

All of the following requests require an Authorization header including an access token, like so:
`Authorization: "Bearer <access_token>"`

### /api/v1.0/notes - GET

#### Accepts:

GET request with authorization header as per above.

#### Returns:

A JSON response including an array of notes.

Example response JSON:
```
{
  "notes": [
    {
      "title": "note title",
      "text": "note text...",
      "owner": "john@doe",
      "id": "<note id>",
      "lastModified": "<modification date>"
    },
    {
      etc...
    }
  ],
  "statusCode": 200
}
```

### /api/v1.0/notes/\<id\> - GET

#### Accepts:

GET request with authorization header as per above.

#### Returns:

A JSON response representing a single note object.

Example response JSON:
```
{
  "title": "note title",
  "text": "note text...",
  "owner": "john@doe",
  "id": "<note id>",
  "lastModified": "<modification date>"
}
```

### /api/v1.0/notes - POST

Creates a new note.

#### Accepts:

GET request with authorization header as per above and a JSON body including the data for the new note (title and text).

Example AJAX request:
```
$.ajax({
  url: <url>,
  crossDomain: true,
  type: 'POST',
  contentType: 'application/JSON',
  data: {
    title: "new title",
    text: "lorem ipsum..."
  },
  headers: { Authorization: 'Basic <access_token>' }
})...
```

#### Returns:

A JSON response including a message indicating success and the data for the newly created note.

Example response JSON:
```
{
  "message": "Note created",
  "statusCode": 201,
  "note": {
    "title": "title",
    "text": "lorem ipsum..."
    "id": "<id>",
    "lastModified": "<modification date>",
    "owner": "john@doe"
  }
}
```

### /api/v1.0/notes/\<id\> - DELETE

Deletes a single note.

#### Accepts

A DELETE request including an authorization header as per above.

#### Returns

A JSON response indicating success.

Example response JSON:
```
{
  "message": "Note <id> deleted",
  "statusCode": 200
}
```

### /api/v1.0/notes/\<id\> - PUT

Updates data on a single note.

#### Accepts

A PUT request with an authorization header as per above and new values for one or both of title and text in the request data.

Example AJAX request:
```
$.ajax({
  url: <url>,
  crossDomain: true,
  type: 'POST',
  contentType: 'application/JSON',
  data: { title: "updated title" },
  headers: { Authorization: 'Basic <access_token>' }
})...
```

#### Returns

A JSON response including a message indicating success and the new note object.

Example response JSON:
```
{
  "message": "Note updated",
  "note": { <node object> },
  "statusCode": 200
}
```
