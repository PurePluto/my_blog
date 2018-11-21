import xadmin
from .models import ReadNum, ReadDetail


class ReadNumAdmin(object):
    list_display = ['read_num', 'content_object']


class ReadDetailAdmin(object):
    list_display = ['date', 'read_num', 'content_object']


xadmin.site.register(ReadNum, ReadNumAdmin)
xadmin.site.register(ReadDetail, ReadDetailAdmin)