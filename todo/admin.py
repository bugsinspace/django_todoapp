from django.contrib import admin
from .models import Todo, Setting

class TodoAdmin(admin.ModelAdmin):
    class Meta:
        model = Todo
        fiels = '__all__'

admin.site.register(Todo, TodoAdmin)
admin.site.register(Setting)
