from django.contrib import admin
from . models import AccountUser, Account, Action

admin.site.register(AccountUser)
admin.site.register(Account)
admin.site.register(Action)