import xadmin
from xadmin import views


class BassSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '博客管理系统'
    site_footer = 'clay'
    menu_style = 'accordion'


class UserProfileAdmin(object):
    list_display = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']
    search_files = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']
    list_filter = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BassSetting)