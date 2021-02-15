from django.contrib import admin
from publication.models import Publication, FavoritePublication

admin.site.register(Publication)
admin.site.register(FavoritePublication)