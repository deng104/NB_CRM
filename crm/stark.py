from stark.service.sites import site, ModelStark
from .models import *
from django.utils.safestring import mark_safe
from django.urls import path
from django.shortcuts import HttpResponse, render
from django import forms

from django.db.models import F, Q, Max, When, Case, Count


class BaseModelForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        # for filed in self.fields.values():
        #     filed.widget.attrs.update({'class': 'form-control'})


class CustomerConfig(ModelStark):

    def display_class_list(self, obj=None, is_header=False):
        if is_header:
            return "所报班级"
        else:
            names = ["{}{}({})".format(obj.get_course_display(), obj.semester, obj.campuses) for obj in
                     obj.class_list.all()]
            return mark_safe("<br>".join(names))

    def status(self, obj=None, is_header=False):
        if is_header:
            return "状态"

        status_color = {
            "studying": "green",
            "signed": "#B03060",
            "unregistered": "red",
            "paid_in_full": "blue"
        }
        return mark_safe(
            "<span style='background-color:%s;color:white;padding:4px;display:inline-block;width:90px'>%s</span>" % (
            status_color[obj.status], obj.get_status_display()))

    def display_consultrecord(self, obj=None, is_header=False):
        if is_header:
            return "跟进记录"
        url = "/stark/crm/consultrecord/?customer=%s" % obj.pk
        return mark_safe("<a href='%s' >跟进记录</a>" % url)

    list_display = ["name", "qq", "source", "consultant", display_consultrecord, display_class_list, status]
    list_filter = ["status", "consultant", "class_list"]
    search_fields = ["name", "qq"]

    def own2public(self, request, queryset):
        queryset.update(consultant=None)

    own2public.desc = "私户转公户"

    def public2own(self, request, queryset):
        queryset.update(consultant=4)

    public2own.desc = "公户转私户"

    def own_customer(self, request):
        data = {
            "actions": [CustomerConfig.own2public, ],
            "list_filter": ["status", "class_list"],
            "queryset": Customer.objects.filter(consultant=request.user.pk),
            "title": "我的客户",
            "add_btn": False,
        }
        res = self.list_view(request, data)
        return res

    def public_customer(self, request):
        data = {
            "actions": [CustomerConfig.public2own, ],
            "list_filter": ["status", "class_list"],
            "queryset": Customer.objects.filter(consultant=None),
            "title": "公海客户",
            "add_btn": False,
        }
        res = self.list_view(request, data)
        return res

    def statistics(self, request):
        date = request.GET.get("date", "today")
        import datetime
        now = datetime.datetime.now().date()
        data = {
            "today": "今日",
            "yesterday": "昨日",
            "week": "近一周",
            "recent_month": "近一月",
        }
        date_show = data.get(date)
        # 1 简单版本
        # UserInfo.objects.filter(depart_id=1,customers__deal_date=now).annotate(c=Count("customers")).values("name","c")
        # 2 完美版本

        ret = UserInfo.objects.filter(depart=1).annotate(
            c=Count(Case(When(customers__deal_date=now, then=F('customers'))))).values_list("name", "c")
        print(ret)
        print('0'*120)
        ret_x = [i[0] for i in ret]
        ret_y = [i[1] for i in ret]

        customer_list = Customer.objects.filter(deal_date=now)
        return render(request, "statistics.html", locals())

    def extra_url(self):
        temp = [
            path('own/', self.own_customer),
            path('public/', self.public_customer),
            path('statistics/', self.statistics),
        ]
        return temp


class ConsultRecordModelForm(BaseModelForm):

    def __init__(self, request, *arg, **kwargs):
        super().__init__(request, *arg, **kwargs)
        customer_choices = [(customer.pk, customer.name) for customer in request.user.customers.all()]
        self.fields['consultant'].widget.choices = [(request.user.pk, request.user.name)]
        self.fields['customer'].widget.choices = customer_choices

    class Meta:
        model = ConsultRecord
        exclude = ["delete_status", ]


class ConsultRecordConfig(ModelStark):
    list_display = ["consultant", "customer", "note", "date", 'status']
    model_form_class = ConsultRecordModelForm


site.register(UserInfo)
site.register(Customer, CustomerConfig)
site.register(Department)
site.register(Campuses)
site.register(Klass)
site.register(ConsultRecord, ConsultRecordConfig)
