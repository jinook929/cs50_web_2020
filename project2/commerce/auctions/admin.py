from .models import *
from django.contrib import admin

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
