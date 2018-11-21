import xadmin
from .models import Category, Blog


class CategoryAdmin(object):
    list_display = ['name']


class BlogAdmin(object):
    list_display = ['id', 'title', 'author', 'category', 'get_read_num', 'content', 'create_time', 'update_time']
    search_files = ['title', 'author', 'category', 'content']
    list_filter = ['title', 'author', 'category', 'content', 'create_time', 'update_time']


xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Blog, BlogAdmin)
