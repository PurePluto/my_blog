import xadmin
from django.utils.translation import ugettext as _
from django.urls.base import reverse, NoReverseMatch
from django.db import models
from xadmin.views.edit import ModelFormAdminUtil
from xadmin.sites import site
from xadmin.util import label_for_field
from xadmin.views import BaseAdminPlugin, ListAdminView


class DetailsPlugin(BaseAdminPlugin):

    show_detail_fields = []
    show_all_rel_details = True

    def result_item(self, item, obj, field_name, row):
        if (self.show_all_rel_details or (field_name in self.show_detail_fields)):
            rel_obj = None
            if hasattr(item.field, 'rel') and isinstance(item.field.rel, models.ManyToOneRel):
                rel_obj = getattr(obj, field_name)
            elif field_name in self.show_detail_fields:
                rel_obj = obj

            if rel_obj:
                if rel_obj.__class__ in site._registry:
                    try:
                        model_admin = site._registry[rel_obj.__class__]
                        has_view_perm = model_admin(self.admin_view.request).has_view_permission(rel_obj)
                        has_change_perm = model_admin(self.admin_view.request).has_change_permission(rel_obj)
                    except:
                        has_view_perm = self.admin_view.has_model_perm(rel_obj.__class__, 'view')
                        has_change_perm = self.has_model_perm(rel_obj.__class__, 'change')
                else:
                    has_view_perm = self.admin_view.has_model_perm(rel_obj.__class__, 'view')
                    has_change_perm = self.has_model_perm(rel_obj.__class__, 'change')

            if rel_obj and has_view_perm:
                opts = rel_obj._meta
                try:
                    item_res_uri = reverse(
                        '%s:%s_%s_detail' % (self.admin_site.app_name,
                                             opts.app_label, opts.model_name),
                        args=(getattr(rel_obj, opts.pk.attname),))
                    if item_res_uri:
                        if has_change_perm:
                            edit_url = reverse(
                                '%s:%s_%s_change' % (self.admin_site.app_name, opts.app_label, opts.model_name),
                                args=(getattr(rel_obj, opts.pk.attname),))
                        else:
                            edit_url = ''
                        item.btns.append('<a data-res-uri="%s" data-edit-uri="%s" class="details-handler" rel="tooltip" title="%s"><i class="fa fa-info-circle"></i></a>'
                                         % (item_res_uri, edit_url, _(u'Details of %s') % str(rel_obj)))
                except NoReverseMatch:
                    pass
        return item

    # Media
    def get_media(self, media):
        if self.show_all_rel_details or self.show_detail_fields:
            media = media + self.vendor('xadmin.plugin.details.js', 'xadmin.form.css')
        return media


class CustomDetailPlugin(BaseAdminPlugin):

    custom_details = {}

    def __init__(self, admin_view):
        super(CustomDetailPlugin, self).__init__(admin_view)
        self.editable_need_fields = {}

    def init_request(self, *args, **kwargs):
        active = bool(self.request.method == 'GET' and self.admin_view.has_view_permission() and self.custom_details)
        if active:
            self.model_form = self.get_model_view(ModelFormAdminUtil, self.model).form_obj
        return active

    def result_item(self, item, obj, field_name, row):
        if self.custom_details and item.field and (field_name in self.custom_details.keys()):
            pk = getattr(obj, obj._meta.pk.attname)
            field_label = label_for_field(field_name, obj, model_admin=self.admin_view, return_attr=False)

            item.wraps.insert(0, '<span class="editable-field">%s</span>')
            title = self.custom_details.get(field_name, {}).get('title', _(u"Details of %s") % field_label)
            default_load_url = self.admin_view.model_admin_url('patch', pk) + '?fields=' + field_name
            load_url = self.custom_details.get(field_name, {}).get('load_url', default_load_url)
            if load_url != default_load_url:
                concator = '?' if load_url.find('?') == -1 else '&'
                load_url = load_url+concator+'pk='+str(pk)
            item.btns.append((
                '<a class="editable-handler" title="{title}" '
                'data-editable-field="{field_name}"'
                'href="{load_url}" target="blank">' +
                '<i class="fa fa-print"></i></a>').format(title=title, field_name=field_name, load_url=load_url))
            # data-editable-field="%s" data-editable-loadurl="%s"
            if field_name not in self.editable_need_fields:
                self.editable_need_fields[field_name] = item.field
        return item

    # Media
    def get_media(self, media):
        if self.editable_need_fields:
            media = media + self.model_form.media + \
                self.vendor(
                    'xadmin.plugin.editable.js', 'xadmin.widget.editable.css')
        return media


site.register_plugin(DetailsPlugin, ListAdminView)
# 2018.05.04 同时，修改了xadmin/static/js/xadmin.plugin.editable.js
# 增加这个插件是为了在列表中增加一个按钮，以实现打印功能。
xadmin.site.register_plugin(CustomDetailPlugin, ListAdminView)
