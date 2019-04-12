from django.conf.urls import url
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from stark.utils.page import Pagination
from django.db.models import Q
from crm.models import *
import copy
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import ManyToManyField, ForeignKey
from django.db.models.fields import DateTimeField, DateField
from django.forms import widgets as wid


class ShowList(object):
    """
    展示类,服务于配置类
    """

    def __init__(self, config_obj, data_list, request):

        self.config_obj = config_obj  # 当前查看表的配置类对象
        self.data_list = data_list
        self.request = request
        # 对展示数据进行分页
        self.page_queryset = self.get_page_queryset()

    def get_page_queryset(self):

        current_page = self.request.GET.get("page", 1)  # 默认首页
        self.pagination = Pagination(current_page, self.data_list.count(), self.request, 10)
        page_queryset = self.data_list[self.pagination.start:self.pagination.end]
        return page_queryset

    def get_headers(self):

        # header_list=["书籍名称","价格","人民出版社"，"操作"]   默认配置类：    ["PUBLISH"]
        header_list = []
        for field_or_func in self.config_obj.new_list_display():  # ["title","price","publish",edit]
            if callable(field_or_func):
                val = field_or_func(self.config_obj, is_header=True)
            else:
                try:
                    filed_obj = self.config_obj.model._meta.get_field(field_or_func)
                    val = filed_obj.verbose_name
                except FieldDoesNotExist as e:
                    val = self.config_obj.model._meta.model_name.upper()

            header_list.append(val)

        return header_list

    def get_body(self):
        # 构建数据表单部分
        new_data_list = []
        for model_obj in self.page_queryset:
            temp = []
            for field_or_func in self.config_obj.new_list_display():

                if callable(field_or_func):
                    val = field_or_func(self.config_obj, model_obj)
                else:
                    try:
                        field_obj = self.config_obj.model._meta.get_field(field_or_func)
                        if isinstance(field_obj, ManyToManyField):
                            rel_data_list = getattr(model_obj, field_or_func).all()
                            l = [str(item) for item in rel_data_list]
                            val = ",".join(l)
                        elif field_obj.choices:
                            val = getattr(model_obj, "get_%s_display" % field_or_func)
                        elif isinstance(field_obj, DateTimeField):
                            val = getattr(model_obj, field_or_func).strftime("%Y-%m-%d")
                        else:
                            val = getattr(model_obj, field_or_func)  # obj.title
                            if field_or_func in self.config_obj.list_display_links:
                                _url = self.config_obj.get_change_url(model_obj)
                                val = mark_safe("<a href='%s'>%s</a>" % (_url, val))

                    except FieldDoesNotExist as e:
                        val = getattr(model_obj, field_or_func)()

                temp.append(val)
            new_data_list.append(temp)

        return new_data_list

    def get_list_filter_links(self):

        list_filter_links = {}

        for field in self.config_obj.list_filter:
            params = copy.deepcopy(self.request.GET)  # 不能放在循环外面

            current_filed_pk = params.get(field, 0)
            field_obj = self.config_obj.model._meta.get_field(field)
            rel_model_queryset = []

            if isinstance(field_obj, ForeignKey) or isinstance(field_obj, ManyToManyField):
                rel_model = field_obj.remote_field.model
                _limit_choices_to = field_obj.remote_field.limit_choices_to
                rel_model_queryset = rel_model.objects.filter(
                    **_limit_choices_to)  # [<Publish: 南京出版社>, <Publish: CCC>, <Publish: 海南出版社>]
                data_list = rel_model_queryset
            else:
                data_list = field_obj.choices

            temp = []
            # 处理 全部标签
            if params.get(field):
                del params[field]
                temp.append("<a class='btn btn-default btn-sm' href='?%s'>全部</a>" % params.urlencode())
            else:
                temp.append("<a  class='btn btn-default btn-sm active' href='#'>全部</a>")

            for obj in data_list:
                if type(obj) == tuple:
                    pk, text = obj[0], obj[1]
                else:
                    pk, text = obj.pk, str(obj)

                params[field] = pk
                if str(pk) == current_filed_pk:
                    link = "<a class='btn btn-default btn-sm active' href='?%s'>%s</a>" % (params.urlencode(), text)
                else:
                    link = "<a class='btn btn-default btn-sm' href='?%s'>%s</a>" % (params.urlencode(), text)
                temp.append(link)
            list_filter_links[field] = [field_obj.verbose_name, temp]

        return list_filter_links


class ModelStark(object):
    """
    默认配置类
    """
    list_display = ["__str__"]
    model_form_class = None
    list_display_links = []
    search_fields = []
    list_filter = []
    actions = []

    def __init__(self, model):
        self.model = model
        self.model_name = self.model._meta.model_name
        self.app_label = self.model._meta.app_label

    # 默认action函数:批量删除
    def patch_delete(self, request, queryset):
        queryset.delete()

    patch_delete.desc = "批量删除"

    # 构建新的action列表
    def get_new_actions(self):

        temp = []
        temp.extend(self.actions)
        temp.append(self.patch_delete)
        new_actions = []
        for func in temp:
            new_actions.append({
                "desc": func.desc,
                "name": func.__name__
            })

        return new_actions

    # 构建新的搜索字段列表
    def get_new_search_fields(self):
        new_search_fields = []
        for item in self.search_fields:
            new_search_fields.append({
                "field_str": item,
                "field_verbose_name": self.model._meta.get_field(item).verbose_name
            })
        return new_search_fields

    # 反向解析当前查看表的增删改查的url
    def get_list_url(self):
        url_name = "%s_%s_list" % (self.app_label, self.model_name)
        _url = reverse(url_name)
        return _url

    def get_add_url(self):
        url_name = "%s_%s_add" % (self.app_label, self.model_name)
        _url = reverse(url_name)
        return _url

    def get_change_url(self, obj):
        url_name = "%s_%s_change" % (self.app_label, self.model_name)
        _url = reverse(url_name, args=(obj.pk,))
        return _url

    def get_del_url(self, obj):
        url_name = "%s_%s_delete" % (self.app_label, self.model_name)
        _url = reverse(url_name, args=(obj.pk,))
        return _url

    # 默认编辑列
    def edit(self, obj=None, is_header=False):
        if is_header:
            return "编辑"
        else:
            return mark_safe(
                "<a href='%s'><i class='fa fa-edit' aria-hidden='true'></i></a>" % self.get_change_url(obj))

    # 默认删除列
    def delete(self, obj=None, is_header=False):
        if is_header:
            return "删除"
        return mark_safe("<a href='%s'><i class='fa fa-trash-o fa-lg'></i></a>" % self.get_del_url(obj))

    # 默认选择列
    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return mark_safe("<input type='checkbox' id='choose'>")
        return mark_safe("<input type='checkbox' name='pk_list' value=%s>" % obj.pk)

    # 构建新的展示列
    def new_list_display(self):
        temp = []
        temp.extend(self.list_display)

        temp.insert(0, ModelStark.checkbox)
        if not self.list_display_links:
            temp.append(ModelStark.edit)
        temp.append(ModelStark.delete)

        return temp

    # 获取搜索的Q对象
    def get_search_condition(self, request):
        val = request.GET.get("q")
        search_field = request.GET.get("search_field")
        search_condition = Q()
        if val:
            search_condition.children.append((search_field + "__icontains", val))

        return search_condition

    # 获取条件过滤的Q对象
    def get_filter_condition(self, request):
        filter_condition = Q()
        for key, val in request.GET.items():
            if key in ["page", "q", "search_field"]:
                continue
            filter_condition.children.append((key, val))

        return filter_condition

    # 查看视图函数
    def list_view(self, request, data=None):

        """
        self :当前访问模型表的配置类对象
        self.model : 当前访问模型表
        self.list_display:当前访问模型表的展示列

        """
        print('666')
        import datetime
        now = datetime.datetime.now().date()
        from django.db.models import Count
        ret = UserInfo.objects.filter(depart_id=1, customers__deal_date=now).annotate(c=Count("customers")).values(
            "name", "c")

        if request.method == "POST":
            pk_list = request.POST.getlist("pk_list")
            queryset = self.model.objects.filter(pk__in=pk_list)
            action = request.POST.get("action")
            if action:
                action = getattr(self, action)
                action(request, queryset)

        if data:
            queryset = data.get("queryset")
            title = data.get("title")
            self.actions = data.get("actions")
            self.list_filter = data.get("list_filter")
            self.add_btn = data.get("add_btn")


        else:
            queryset = self.model.objects.all()  # Book.objects.all()
            title = self.model._meta.verbose_name
            self.actions = self.__class__.__dict__.get("actions", [])
            self.list_filter = self.__class__.__dict__.get("list_filter", [])
            self.add_btn = True

        # 展示页面相关变量
        add_url = self.get_add_url()
        # 获取搜索条件对象
        search_condition = self.get_search_condition(request)
        # 获取filter的condition
        filter_condition = self.get_filter_condition(request)
        # 数据过滤
        data_list = queryset.filter(search_condition).filter(filter_condition)
        # 将过滤数据分页展示表头和表体
        showlist = ShowList(self, data_list, request)

        return render(request, "stark/list_view.html", locals())

    def get_new_form(self, form):
        from django.forms.boundfield import BoundField
        from django.forms.models import ModelChoiceField
        for bfield in form:

            if isinstance(bfield.field, ModelChoiceField):
                print(">>>", type(bfield.field))
                bfield.is_pop = True
                rel_model = self.model._meta.get_field(bfield.name).remote_field.model
                model_name = rel_model._meta.model_name
                app_label = rel_model._meta.app_label
                if app_label == "auth":
                    continue
                _url = reverse("%s_%s_add" % (app_label, model_name))
                bfield.url = _url
                bfield.pop_back_id = "id_" + bfield.name

        return form

    # 动态获取ModelForm
    def get_model_form(self, request):

        class DefaultModelForm(forms.ModelForm):
            def __init__(self, request=request, *args, **kwargs):
                self.request = request
                super().__init__(*args, **kwargs)

            class Meta:
                model = self.model
                fields = "__all__"

        return self.model_form_class or DefaultModelForm

    # 添加视图函数
    def add_view(self, request):
        current_model_name = self.model._meta.verbose_name
        ModelFormClass = self.get_model_form(request)
        is_pop = request.GET.get("pop")

        if request.method == "POST":

            form = ModelFormClass(request, request.POST)
            form = self.get_new_form(form)
            if form.is_valid():
                obj = form.save()
                if is_pop:
                    text = str(obj)
                    pk = obj.pk
                    return render(request, "stark/pop.html", locals())
                else:
                    return redirect(self.get_list_url())

            return render(request, "stark/add_view.html", locals())

        form = ModelFormClass(request)
        form = self.get_new_form(form)

        return render(request, "stark/add_view.html", locals())

    # 编辑视图函数
    def change_view(self, request, id):
        current_model_name = self.model._meta.verbose_name
        ModelFormClass = self.get_model_form(request)
        edit_obj = self.model.objects.get(pk=id)

        if request.method == "POST":
            form = ModelFormClass(request, data=request.POST, instance=edit_obj)
            form = self.get_new_form(form)
            if form.is_valid():
                form.save()  # update
                return redirect(self.get_list_url())

            return render(request, "stark/change_view.html", locals())

        form = ModelFormClass(request, instance=edit_obj)
        form = self.get_new_form(form)
        return render(request, "stark/change_view.html", locals())

    # 删除视图函数
    def del_view(self, request, id):

        if request.method == "POST":
            self.model.objects.filter(pk=id).delete()
            return redirect(self.get_list_url())

        list_url = self.get_list_url()
        return render(request, "stark/del_view.html", locals())

    # 额外URL的接口
    def extra_url(self):

        return []

    # url的二级分发
    def get_urls(self):

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        temp = [

            url(r"^$", self.list_view, name="%s_%s_list" % (app_label, model_name)),
            url(r"add/", self.add_view, name="%s_%s_add" % (app_label, model_name)),
            url(r"(\d+)/change/", self.change_view, name="%s_%s_change" % (app_label, model_name)),
            url(r"(\d+)/delete/", self.del_view, name="%s_%s_delete" % (app_label, model_name)),

        ]

        temp.extend(self.extra_url())

        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


class StarkSite(object):
    """
    stark组件的全局类
    """

    def __init__(self):
        self._registry = {}

    # 1 模型类的注册功能
    def register(self, model, admin_class=None):
        # 设置配置类
        admin_class = admin_class or ModelStark
        self._registry[model] = admin_class(model)

    # 2 动态创建模型类的增删改查URL
    def get_urls(self):
        temp = []
        for model, config_obj in self._registry.items():
            model_name = model._meta.model_name  # "book"
            app_label = model._meta.app_label  # "app01"
            # url的一级分发
            temp.append(url(r"%s/%s/" % (app_label, model_name), config_obj.urls))

            '''
            temp=[

                # (1) url(r"app01/book/",BookConfig(Book).urls)
                # (2) url(r"app01/book/",(BookConfig(Book).get_urls(), None, None))
                # (3) url(r"app01/book/",([
                                                url(r"^$", BookConfig(Book).listview),
                                                url(r"add/$", BookConfig(Book).addview),
                                                url(r"(\d+)/change/$", BookConfig(Book).changeview),
                                                url(r"(\d+)/delete/$", BookConfig(Book).delview),
                                         ], None, None))

                ###########

                # url(r"app01/publish/",([
                                                url(r"^$", ModelStark(Publish).listview),
                                                url(r"add/$",  ModelStark(Publish).addview),
                                                url(r"(\d+)/change/$",  ModelStark(Publish).changeview),
                                                url(r"(\d+)/delete/$",  ModelStark(Publish).delview),
                                         ], None, None))
            ]

            '''

        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


site = StarkSite()

'''
************************************************************
这里有两个问题,也是整个组件中最核心的两个问题:
    1 为什么需要配置类,配置信息放在全局类StarkSite中不好吗?
    2 二级分发为什么放在配置类中,直接在StarkSite中进行有坑吗?
************************************************************
'''


def list_view(self, request, new_queryset=None, flag=False):
    self.request = request
    if request.method == "POST":
        # action 处理
        patch_func_str = request.POST.get("patch_func")
        choose_pk = request.POST.getlist("choose_pk")
        queryset = self.model.objects.filter(pk__in=choose_pk)
        print(patch_func_str, choose_pk)  # patch_delete ['4', '6']
        patch_func = getattr(self, patch_func_str)
        res = patch_func(request, queryset)
        if res:
            return res

    if flag:
        queryset = new_queryset
    else:
        queryset = self.model.objects.all()  # Book.objects.all()

    show_list = ShowList(self, request, queryset)

    # 获取模型变量信息
    table_name = self.model._meta.verbose_name
    add_url = self.get_add_url()

    return render(request, "stark/list_view.html", locals())
