

auth_exaption = {    
    401: {"description": "Unauthorized: Invalid or expired token or user not logged in"},
    403: {"description": "Forbidden: User role not authorized"},
    409: {"description": "Conflict: User already logged in on another device"},
    200: {"description": "Success: User information retrieved"},
    }

singup_exaption = {
    409: {"description": "user name or shop name already exist"}
}

login_exaption = {
    404: {"description": "user name does not exist"},
    401: {"description": "Incorrect password"}
}