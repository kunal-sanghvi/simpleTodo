from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import request, JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .authorizer import basic_auth, create_token, jwt_auth, log_out
from .models import Todo


@require_GET
@basic_auth
def login(req: request, user: User):
    if settings.JWT_CACHE.exists(user.username):
        return JsonResponse({'message': 'already logged in! if token lost, contact admin for force logout'}, status=403)
    ttl = timedelta(minutes=settings.JWT_EXPIRY_DURATION)
    access_token, expiry_time = create_token(user.username, ttl)
    settings.JWT_CACHE.setex(user.username, ttl, access_token)
    return JsonResponse({
        'message': 'log in success',
        'access_token': access_token,
        'expiry_time': expiry_time.isoformat()
    })


@require_http_methods(['DELETE'])
@jwt_auth
def logout(req: request, user: User):
    log_out(user.username)
    return JsonResponse({'message': 'log out success'}, status=200)


@require_GET
@jwt_auth
def list_todo(req: request, user: User):
    paginator = Paginator(Todo.objects.filter(user=user), settings.PAGE_SIZE)
    objects = paginator.page(req.GET.get('page', 1))
    todos = []
    for todo in objects:
        todos.append({'task': todo.task, 'id': todo.pk})
    return JsonResponse({'todos': todos})


@require_POST
@jwt_auth
def create_todo(req: request, user: User, data: dict):
    Todo.objects.create(user=user, task=data.get('task'))
    return JsonResponse({'message': 'created'})


@require_http_methods(['DELETE'])
@jwt_auth
def delete_todo(req: request, user: User, pk: int):
    try:
        Todo.objects.get(pk=pk, user=user).delete()
    except Todo.DoesNotExist:
        return JsonResponse({'message': 'not found'}, status=400)
    return JsonResponse({'message': 'deleted'})
