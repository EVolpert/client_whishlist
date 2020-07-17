from django.contrib import admin
from whishlist.models import Whishlist


@admin.register(Whishlist)
class WhishlistAdmin(admin.ModelAdmin):
    pass