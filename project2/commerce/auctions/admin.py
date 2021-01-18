from .models import *
from django.contrib import admin

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ListingAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at',)

class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment, CommentAdmin)
