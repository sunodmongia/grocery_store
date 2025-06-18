from django.contrib import admin
from .models import *


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Movement_of_Items)

