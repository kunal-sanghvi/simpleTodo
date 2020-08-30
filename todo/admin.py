from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from django.http import HttpResponseRedirect
from .authorizer import is_logged_in, log_out
from .models import Todo


class TodoAdmin(admin.ModelAdmin):

    list_display = ('task', 'user')


class TodoUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_logged_in')

    change_form_template = 'user_change_form.html'

    def response_change(self, request, instance):
        if '_force_todo_logout' in request.POST:
            log_out(instance.username)
            self.message_user(request, 'User {} is forcefully logged out'.format(instance.username))
            return HttpResponseRedirect(".")
        return super().response_change(request, instance)

    def get_logged_in(self, instance):
        return is_logged_in(instance.username)

    get_logged_in.boolean = True
    get_logged_in.short_description = 'Logged In'


admin.site.register(Todo, TodoAdmin)
admin.site.unregister(User)
admin.site.register(User, TodoUserAdmin)
