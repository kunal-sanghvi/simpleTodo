<h1 align="center">SimpleTodo 📝</h1>

> Django App powering User to manage his todos, after requesting an access_token during login step. Admin can force logout users as needed

## Setup
```
 $ pip install requirements.txt
 $ python manage.py makemigrations
 $ python manage.py migrate
 $ python manage.py createsuperuser
 $ python manage.py runserver
```

## Documentation

#### Login

*AuthType*: Basic Auth (your username and password)

*Path*: `GET /login/`

*Sample Response*
```
200 OK
{
    "message": "log in success",
    "access_token": "<token which will expire in 10 minutes (configurable)>",
    "expiry_time": "2020-08-31T14:30:57.069644"
}
```
--------------------

> **Note**: From here on the access_token will be referenced as ```$access_token```

--------------------

#### List All Todos

*AuthType*: Token based authentication (add a header with key as `X-TODO-APP-JWT` and value as `$access_token`)

*Path*: `GET /todos/`

*Sample Response*
```
200 OK
{
    "todos": [
        {
            "task": "todo 0",
            "id": 541
        },
        {
            "task": "todo 1",
            "id": 542
        }
    ]
}
```

--------------------

#### Create Todo

*AuthType*: JWT (add a header with key as `X-TODO-APP-JWT` and value as `$access_token`)

*Path*: `POST /todos/create/`

*Sample Request Body*
```
{
    "task": "create google app"
}
```


*Sample Response*
```
200 OK
{
    "message": "created"
}
```

--------------------

#### Delete Todo

*AuthType*: Token based authentication (add a header with key as `X-TODO-APP-JWT` and value as `$access_token`)

*Path*: `DELETE /todos/< todo ID received during list response >/`

*Sample Response*
```
200 OK
{
    "message": "deleted"
}
```

--------------------

#### Logout

*AuthType*: Token based authentication (add a header with key as `X-TODO-APP-JWT` and value as `$access_token`)

*Path*: `DELETE /logout/`

*Sample Response*
```
200 OK
{
    "message": "log out success"
}
```

--------------------

## Token Lifecycle
```
403 Forbidden
{
    "message": "your current token has expired, please login again"
}
```
1. The token expires in 10 minutes. Can be configured to some other value by setting `JWT_EXPIRY_DURATION` env variable
2. In case you lose the access token, only admin has the authority to force expire your token

## Extra admin functions

> Goto admin console -> users page (`/admin/auth/user/`)

![Admin console list user view](https://github.com/kunal-sanghvi/simpleTodo/blob/master/img/UserListView.png?raw=true)

> Open edit user data page for any user whom you want to force logout, you'd see a ``FORCE LOGOUT`` button at the bottom of the screen

![Admin console list user view](https://github.com/kunal-sanghvi/simpleTodo/blob/master/img/UserForceLogout.png?raw=true)