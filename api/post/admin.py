# 2023-02-16
# post/admin.py

from django.contrib import admin

from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    model = Post

    def categories(self, obj):
        return obj.get_category_item_list()
    categories.short_description = 'Categories'

    list_display = ('id', 'description', 'categories')
    list_filter = ('author', )

# admin.site.register(Post, PostAdmin)
admin.site.register(Category)
class PostAdmin(admin.ModelAdmin):
    model = Post
    def node_id(self, obj):
        return obj.get_node_id()
    node_id.short_description = 'Node Id'

    def author_name(self, obj):
        return obj.author.display_name if obj.author.display_name else obj.author.username
    author_name.short_description = 'Author'

    date_hierarchy = 'updated_at'
    list_editable = ('visibility', 'unlisted',)
    list_display = ('node_id', 'author_name', 'title', 'description', 'content_type', 'visibility', 'unlisted', 'updated_at')
    list_filter = ('author__display_name', 'author__username', 'content_type', 'updated_at')
    search_fields = ('id', 'title')
    ordering = ('id', 'title')

admin.site.register(Post, PostAdmin)
