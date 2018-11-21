import xadmin
from .models import Comment


class CommentAdmin(object):
    list_display = ['content_object', 'text', 'comment_time', 'user']


xadmin.site.register(Comment, CommentAdmin)