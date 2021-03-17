SUCCESS_200 = {
    'http_code': 200,
    'status': 'success'
}
SUCCESS_201 = {
    'http_code': 201,
    'status': 'success'
}
SUCCESS_204 = {
    'http_code': 204,
    'status': 'success'
}
MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "status": "missingParameter",
    "message": "Missing parameters."
}
BAD_REQUEST_400 = {
    "http_code": 400,
    "status": "badRequest",
    "message": "Bad request"
}
SERVER_ERROR_500 = {
    "http_code": 500,
    "status": "serverError",
    "message": "Server error"
}
SERVER_ERROR_404 = {
    "http_code": 404,
    "status": "notFound",
    "message": "Resource not found"
}
UNAUTHORIZED_403 = {
    "http_code": 403,
    "status": "notAuthorized",
    "message": "You are not authorised to execute this."
}
INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "status": "invalidField",
    "message": "Invalid fields found"
}
INVALID_INPUT_422 = {
    "http_code": 422,
    "status": "invalidInput",
    "message": "Invalid input"
}
