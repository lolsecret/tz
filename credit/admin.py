from django.contrib import admin
from .models import Program, Application, Blacklist, Borrower
# Register your models here.
admin.site.register(Program)
admin.site.register(Borrower)
admin.site.register(Application)
admin.site.register(Blacklist)
