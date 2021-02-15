from django.contrib import admin
from news_npo.models import News, ConfirmationCode, User, FavoriteNews, NewsImage

class ImageInLIne(admin.StackedInline):
    model = NewsImage
    extra = 1


class NewsAdmin(admin.ModelAdmin):
    model = News
    list_filter = 'created_date'.split()
    list_editable = 'title'.split()
    list_display = 'id title image link created_date'.split()
    search_fields = 'title description'.split()
    inlines = [ImageInLIne]

admin.site.register(News, NewsAdmin)
admin.site.register(ConfirmationCode)
admin.site.register(User)
admin.site.register(FavoriteNews)
admin.site.register(NewsImage)