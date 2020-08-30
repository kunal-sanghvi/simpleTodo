from django.contrib.auth.models import User
from todo.models import Todo


def run():
    for x in range(50):
        username = 'test_user_{}'.format(x)
        email = 'user_{}@todo.com'.format(x)
        password = 'password_{}'.format(x)
        user = User.objects.create_user(username, email=email, password=password)
        for y in range(30):
            Todo.objects.create(user=user, task='todo {}'.format(y))
