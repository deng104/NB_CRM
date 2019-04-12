from stark.service.sites import site

from .models import *

from stark.service.sites import site, ModelStark

from rbac.models import *
from django import forms
from django.urls.resolvers import URLPattern
from django.conf.urls import url
from django.forms import widgets as wid
from django.shortcuts import HttpResponse, render, redirect
from rbac.models import Role, Permission
from crm.models import UserInfo
from django.http import JsonResponse
import json


class BaseModelForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)


class PermissionModelForm(BaseModelForm):
    class Meta:
        model = Permission
        exclude = ["pids"]
        widgets = {
            "url": wid.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from AcmeCrm.urls import urlpatterns
        ret = [[i, i] for i in self.get_all_url(urlpatterns, prev='/', is_first=True)]
        ret.insert(0, ["", ""])
        self.fields['url'].widget.choices = ret

    def get_all_url(self, urlparrentens, prev, is_first=False, result=[]):
        if is_first:
            result.clear()
        ignore_list = ["admin/"]
        for item in urlparrentens:
            if isinstance(item, URLPattern):
                if str(item.pattern) == "^$":
                    result.append(prev)
                else:
                    result.append(prev + str(item.pattern))
            else:
                if str(item.pattern) in ignore_list: continue
                self.get_all_url(item.urlconf_name, prev + str(item.pattern))

        return result


class PermissionConfig(ModelStark):
    list_display = ['title', "type", 'url', "parent"]
    model_form_class = PermissionModelForm

    def permission_distribute(self, request):

        uid = request.GET.get('uid')
        rid = request.GET.get('rid')
        user = UserInfo.objects.filter(id=uid)

        if request.method == "POST" and request.POST.get('postType') == 'role':
            print(request.POST.getlist("roles"))
            l = request.POST.getlist("roles")
            user.first().roles.set(l)

        if request.method == "POST" and request.POST.get('postType') == 'permission':

            role = Role.objects.filter(id=rid).first()
            if not role:
                return HttpResponse('角色不存在')
            permissions_id_list = request.POST.getlist('permissions_id')
            pids_list = []
            for per_id in permissions_id_list:
                pids = Permission.objects.get(pk=per_id).pids.split("/")
                pids.append(per_id)
                pids_list.extend(pids)

            pids_list = list(set(pids_list))
            role.permissions.set(pids_list)

        # 所有用户
        user_list = UserInfo.objects.all()
        role_list = Role.objects.all()

        if uid:
            role_id_list = UserInfo.objects.get(pk=uid).roles.all().values_list("pk")
            role_id_list = [item[0] for item in role_id_list]
            per_id_list = UserInfo.objects.get(pk=uid).roles.filter(permissions__isnull=False).values_list(
                "permissions__pk").distinct()
            per_id_list = [item[0] for item in per_id_list]

        if rid:
            per_id_list = Role.objects.filter(pk=rid).filter(permissions__isnull=False).values_list(
                "permissions__pk").distinct()
            per_id_list = [item[0] for item in per_id_list]

        permissions_tree = list(Permission.objects.values("pk", "title", "url", "parent", "type"))
        permissions_tree_json = json.dumps(permissions_tree)

        return render(request, "rbac/permission_distribute.html", locals())

    def extra_url(self):
        l = [
            url(r"distribute/", self.permission_distribute),
        ]
        return l


site.register(User)
site.register(Role)
site.register(Permission, PermissionConfig)
