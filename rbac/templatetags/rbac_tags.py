

from django.utils.safestring import mark_safe
from django.template import Library
import json
import collections
import re

from rbac.models import Permission

register = Library()

@register.inclusion_tag("rbac/menu.html")
def get_menu_style(request):

    permission_list = request.session.get("permission_list",[])
    current_path=request.path
    # 构建新的权限字典
    new_permission_dict=collections.OrderedDict()
    for permission_dict in permission_list:
        print(">>>",permission_dict.get("type"))
        if permission_dict.get("type") == "button":
            continue
        temp={}
        temp["id"]=permission_dict.get("id")
        temp["text"]=permission_dict.get("title")
        temp["href"]=permission_dict.get("url") or ""
        temp["pid"]=permission_dict.get("pid")  or ""
        # temp["nodes"]=[]

        if current_path == temp["href"]:
            temp["backColor"] = "#636363"
            temp["color"] = "#fff"

        new_permission_dict[permission_dict.get("id")]=temp

    print("new_permission_dict",new_permission_dict)
    # 构建权限树列表
    permission_tree=[]
    for permission_pk,permission_dict in new_permission_dict.items():
        pid= permission_dict.get("pid")
        if pid:
            # new_permission_dict[pid]["nodes"].append(permission_dict)
            # 去除实际权限的图标
            print(">>>permission_dict",permission_dict)
            print(">>>pid",pid)
            print(">>>new_permission_dict",dict(new_permission_dict))
            if "nodes" in new_permission_dict[pid]:
                new_permission_dict[pid]["nodes"].append(new_permission_dict[permission_pk])
            else:
                new_permission_dict[pid]["nodes"] = [new_permission_dict[permission_pk], ]

        else:
            permission_tree.append(new_permission_dict[permission_pk])


        # 展开访问权限节点
        current_path = request.path
        if current_path == permission_dict.get("href"):
            pid = permission_dict.get("pid")
            while pid:
                new_permission_dict[pid]["state"]={"expanded":True}
                pid=new_permission_dict[pid]["pid"]

    return {"permission_tree":json.dumps(permission_tree)}



@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()