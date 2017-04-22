# API endpoints

## Errors

All endpoints return JSON including descriptive error messages and appropriate status codes, usually formatted like so:
```
{
  'error': 'Login failed (incorrect email or password)',
  'statusCode': 403
}
```

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
