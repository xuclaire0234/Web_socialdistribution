# 2023-03-18
# api/follower/admin.py

from django.contrib import admin
from .models import Follower

class FollowerAdmin(admin.ModelAdmin):
    model = Follower

    def followee_name(self, obj):
        return obj.followee.display_name if obj.followee.display_name else obj.followee.username
    followee_name.short_description = 'Followee'

    def followee_node_id(self, obj):
        return obj.followee.get_node_id()
    followee_node_id.short_description = 'Followee Node Id'

    date_hierarchy = 'followed_at'
    list_display = ('follower_node_id', 'followee_name', 'followee_node_id', 'followed_at')
    list_filter = ('followee', 'follower_node_id')
    search_fields = ('follower_node_id', 'followee__display_name', 'followee__username')
    ordering = ('followee',)

admin.site.register(Follower, FollowerAdmin)
