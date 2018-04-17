from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Compute)
admin.site.register(Database)
admin.site.register(Dbms)
admin.site.register(SoftwareComponent)
admin.site.register(WebApplication)
admin.site.register(WebServer)
admin.site.register(Template)