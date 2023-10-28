errors = {  # Ranges: -inf to 99 error, 100 to inf warning
    'ERR_INVALID_REQUEST': 3,
    'ERR_USER_NOT_FOUND': 10,
    'ERR_USER_NOT_AUTHENTICATED': 11,
    'ERR_USER_STATUS_INSUFFICIENT': 12,
    'WARN_USER_LACKING_GUARDIAN': 110,
    'WARN_INVALID_ROLE': 120,
}

error_texts = {
    -1: "(unresolved name): ",  # In case code is not found
    3: "Invalid request",
    10: "User not found",
    11: "User not authenticated",
    12: "User of insufficient status",
    110: "User lacks guardian",
    120: "User has an invalid role",
}


reverse_errors = {}
for k in errors:
    reverse_errors[errors[k]] = k


def get_error_text(code, suffix=""):
    prefix = ""
    if code >= 100:
        prefix = "Warning: "
    else:
        prefix = "Error: "
    prefix += "(ERRNO " + str(code) + ") "
    
    punctiation = '.'
    if suffix:
        punctiation = ': '
    
    if code in error_texts.keys():
        return prefix + error_texts[code] + punctiation + suffix
    else:
        return prefix + error_texts[-1] + reverse_errors[code] + punctiation + suffix
