import jwt
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class UnauthorizedException(APIException):
    status_code = 401
    default_detail = {"detail": "Token Not provided!"}
    default_code = "not_authenticated"


class CRUDPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise UnauthorizedException()
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            request.GET._mutable = True
            request.GET['user_id'] = payload['id']
            return True
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
