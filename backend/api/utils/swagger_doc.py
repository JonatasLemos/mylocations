LOCATION_TYPE_LIST_200 = {
    "description": "Successful retrieval. Returns a paginated list of location types.",
    "content": {
        "application/json": {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "name": "Landscape",
                        "created_at": "2023-10-27T10:00:00Z",
                    },
                    {
                        "id": 2,
                        "name": "Park",
                        "created_at": "2023-10-28T11:00:00Z",
                    },
                ],
                "total": 2,
                "page": 1,
                "size": 10,
                "pages": 1,
            }
        }
    },
}

LOCATION_TYPE_DETAIL_200 = {
    "description": "Successful retrieval. Returns the location type details.",
    "content": {
        "application/json": {
            "example": {
                "id": 1,
                "name": "Landscape",
                "created_at": "2023-10-27T10:00:00Z",
            }
        }
    },
}

LOCATION_DETAIL_200 = {
    "description": "Successful retrieval. Returns the location details.",
    "content": {
        "application/json": {
            "example": {
                "id": 1,
                "location_type_id": 2,
                "latitude": 1,
                "longitude": 2,
                "created_at": "2023-10-27T10:00:00Z",
            }
        }
    },
}

USER_LOCATION_LIST_200 = {
    "description": "Successful retrieval. Returns a paginated list of locations.",
    "content": {
        "application/json": {
            "example": {
                "items": [
                    {
                        "user_location_id": 1,
                        "location_id": 1,
                        "location_name": "My location",
                        "description": "This is my location.",
                        "latitude": 10,
                        "longitude": 10,
                        "location_type_id": 1,
                        "location_type_name": "Landscape",
                    },
                    {
                        "user_location_id": 2,
                        "location_id": 2,
                        "location_name": "My location 2",
                        "description": "This is my location 2.",
                        "latitude": 12,
                        "longitude": 7,
                        "location_type_id": 1,
                        "location_type_name": "Landscape",
                    },
                ],
                "total": 2,
                "page": 1,
                "size": 10,
                "pages": 1,
            }
        }
    },
}

LOCATION_LIST_200 = {
    "description": "Successful retrieval. Returns a paginated list of locations.",
    "content": {
        "application/json": {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "location_type_id": 1,
                        "latitude": 10,
                        "longitude": 10,
                        "created_at": "2025-03-14T04:23:07.296834",
                    },
                    {
                        "id": 2,
                        "location_type_id": 1,
                        "latitude": 12,
                        "longitude": 7,
                        "created_at": "2025-03-14T05:24:24.694559",
                    },
                ],
                "total": 2,
                "page": 1,
                "size": 10,
                "pages": 1,
            }
        }
    },
}

USER_LOCATION_PATCH_REPONSE = {
    "description": "Succesful update.",
    "content": {
        "application/json": {
            "example": {
                "id": 1,
                "name": "Location name",
                "created_at": "2025-03-14T04:23:07.306968",
                "location_id": 1,
                "user_id": 14,
                "description": "Location description",
            }
        }
    },
}

BAD_REQUEST_400 = {
    "description": "Malformed request.",
    "content": {"application/json": {"example": {"detail": "Invalid request."}}},
}
UNAUTHORIZED_401 = {"description": "Authentication failed."}
FORBIDEN_403 = {"description": "Not authenticated."}
NOT_FOUND_404 = {
    "description": "Object not found.",
    "content": {"application/json": {"example": {"detail": "Object not found."}}},
}
REFRESH_TOKEN_200_RESPONSE = {
    "description": "Succesful refresh token retrieval.",
    "content": {
        "application/json": {
            "example": {
                "access_token": "token",
                "token_type": "bearer",
            }
        }
    },
}
AUTHENTICATION_TOKEN_200_RESPONSE = {
    "description": "Succesful authentication.",
    "content": {
        "application/json": {
            "example": {
                "access_token": "token",
                "refresh_token": "token",
                "token_type": "bearer",
            }
        }
    },
}
