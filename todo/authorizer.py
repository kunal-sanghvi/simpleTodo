import base64
import json
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from typing import Optional


TokenExpired = JsonResponse({'message': 'your current token has expired, please login again'}, status=403)
UnAuthorized = JsonResponse({'message': 'your credentials are not valid'}, status=401)
SorryWeAreDown = JsonResponse({'message': 'something terrible happened and we are down, Sorry!'}, status=500)
WhoAreYou = JsonResponse({'message': 'we need to see your ID!!'}, status=401)


def extract_credentials(request) -> (Optional[str], Optional[str]):
    auth_header = request.META.get('HTTP_AUTHORIZATION', None)
    if auth_header is None:
        return None, None
    encoded_credentials = auth_header.split(' ')[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
    return decoded_credentials[0], decoded_credentials[1]


def basic_auth(func):
    def wrapper(request, *args, **kwargs):
        try:
            username, password = extract_credentials(request)
            if not username or not password:
                return WhoAreYou
            user = authenticate(request=request, username=username, password=password)
        except Exception:
            return SorryWeAreDown
        if user is None:
            return UnAuthorized
        return func(request, user, *args, **kwargs)
    return wrapper


def jwt_auth(func):
    def wrapper(request, *args, **kwargs):
        try:
            jwt_token = request.META.get('HTTP_X_TODO_APP_JWT', None)
            if not jwt_token:
                return WhoAreYou
            jwt_payload = validate_token(jwt_token)
            if not jwt_payload:
                return TokenExpired
            user = User.objects.get(username=jwt_payload.get('user'))
            token = settings.JWT_CACHE.get(user.username)
            if not token:
                return TokenExpired
            if token.decode('utf-8') != jwt_token:
                return TokenExpired
            if request.method == 'POST':
                kwargs['data'] = json.loads(request.body)
            return func(request, user, *args, **kwargs)
        except Exception:
            return SorryWeAreDown
    return wrapper


def create_token(username: str, ttl: timedelta) -> (str, datetime):
    exp = datetime.utcnow() + ttl
    access_token = jwt.encode(payload={'user': username, 'exp': exp.timestamp()},
                              key=settings.JWT_SECRET).decode('utf-8')
    return access_token, exp


def validate_token(token) -> Optional[dict]:
    try:
        return jwt.decode(token, key=settings.JWT_SECRET, verify=True, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None


def is_logged_in(username: str):
    token = settings.JWT_CACHE.get(username)
    if not token:
        return False
    if not validate_token(token):
        return False
    return True


def log_out(username: str):
    settings.JWT_CACHE.delete(username)
