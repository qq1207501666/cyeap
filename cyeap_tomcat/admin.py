from django.contrib import admin
from cyeap_tomcat import models
# Register your models here.

admin.site.register(models.TomcatWebapp)
admin.site.register(models.TomcatServer)
