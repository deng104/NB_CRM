


from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
from rbac.models import Permission
import re

class PermissionMiddleWare(MiddlewareMixin):

    def process_request(self,request):
        print("permission_list",request.session.get("permission_list"))

        current_path = request.path
        # 1 设置白名单放行
        for reg in  ["/home/","/logout/","/login/","/admin/.*","/stark/rbac/.*"]:
            if re.search("^%s$"%reg,current_path):
                return None

        # 2 校验是否登录
        if not request.user.id:
            return redirect("/login/")

        # 3 校验权限
        permission_list=request.session.get("permission_list")
        '''
        permission_list=[
        
          {"url":"","id","pid":""},
          {"url":"","id","pid":""},
          {"url":"","id","pid":""},
    
        ]
        '''

        for item in permission_list:
             reg="^%s$"%item["url"]
             print("current_path",current_path)
             ret=re.search(reg,current_path)
             if ret:
                 return None

        return HttpResponse("无访问权限！")

