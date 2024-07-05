from django.contrib import admin

from organisations.models import Organisation, UserOrganisation

admin.site.register(Organisation)
admin.site.register(UserOrganisation)


# Register your models here.
