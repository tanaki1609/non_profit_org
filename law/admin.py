from django.contrib import admin
from law.models import Law, FavoriteLaw

admin.site.register(Law)
admin.site.register(FavoriteLaw)