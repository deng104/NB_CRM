from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from rbac.models import User

class_type_choices = (('fulltime', '线下班',),
                      ('online', '网络班'),
                      ('weekend', '周末班',))

course_choices = (('设计', '设计初级班'),
                  ('美学', '美学初级班'))

source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('website_luffy', "美啊官网"),
               ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

seek_status_choices = (('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'),)

attendance_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('absence', "缺勤"),
                      ('leave_early', "早退"),)

score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, ' D'),
                 (-1, 'N/A'),
                 (-100, 'COPY'),
                 (-1000, 'FAIL'),)

record_choices = (
    ('checked', "已签到"),
    ('vacate', "请假"),
    ('late', "迟到"),
    ('noshow', "缺勤"),
    ('leave_early', "早退"),
)


#########################  客户管理系统   ###########################################


class UserInfo(AbstractUser, User):
    """
    员工表
    """
    name = models.CharField(max_length=32, unique=True, null=True, verbose_name="姓名")
    birthday = models.DateField(verbose_name='生日', blank=True, null=True)
    age = models.IntegerField(verbose_name='年龄', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('Female', '女'), ('Male', '男')), verbose_name='性别',
                              default='Male')
    image = models.ImageField(upload_to='images/%Y/%m', verbose_name='头像', null=True, blank=True)
    depart = models.ForeignKey("Department", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '员工表'
        verbose_name_plural = '员工表'


class Department(models.Model):
    """
    部门表
    """
    name = models.CharField(max_length=32)
    campuse = models.ForeignKey("Campuses", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.name


class Campuses(models.Model):
    """
    校区表
    """
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '校区'
        verbose_name_plural = '校区'


class Customer(models.Model):
    """
    客户表
    """
    qq = models.CharField('QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True)
    name = models.CharField('姓名', max_length=32, blank=True, null=True, help_text='学员报名后，请改为真实姓名')
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField("性别", choices=sex_type, max_length=16, default='male', blank=True, null=True)
    birthday = models.DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)
    phone = models.BigIntegerField('手机号', blank=True, null=True)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')
    introduce_from = models.ForeignKey('Customer', verbose_name="转介绍自学员", blank=True, null=True,
                                       on_delete=models.CASCADE)
    class_type = models.CharField("班级类型", max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = models.TextField("客户备注", blank=True, null=True, )
    status = models.CharField("状态", choices=enroll_status_choices, max_length=64, default="unregistered",
                              help_text="选择客户此时的状态")
    date = models.DateTimeField("咨询日期", auto_now_add=True)
    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True)
    deal_date = models.DateTimeField("成交日期", blank=True, null=True)
    consultant = models.ForeignKey('UserInfo', verbose_name="销售", related_name='customers', blank=True, null=True,
                                   on_delete=models.CASCADE, limit_choices_to={"depart_id": 1})
    class_list = models.ManyToManyField('Klass', verbose_name="已报班级", blank=True)

    def __str__(self):
        return str(self.name)

    def get_classlist(self):
        l = []
        for cls in self.class_list.all():
            l.append(str(cls))
        return mark_safe("<br>".join(l))

    def get_status(self):
        status_color = {
            "studying": "green",
            "signed": "#B03060",
            "unregistered": "red",
            "paid_in_full": "blue"
        }
        return mark_safe(
            "<span style='background-color:%s;color:white;padding:4px;display:inline-block;width:90px'>%s</span>" % (
            status_color[self.status], self.get_status_display()))

    class Meta:
        verbose_name = '客户列表'
        verbose_name_plural = '客户列表'


class ConsultRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey('Customer', verbose_name="所咨询客户", on_delete=models.CASCADE)
    note = models.TextField(verbose_name="跟进内容...")
    status = models.CharField("跟进状态", max_length=8, choices=seek_status_choices, help_text="选择客户此时的状态")
    consultant = models.ForeignKey("UserInfo", verbose_name="跟进人", related_name='records', on_delete=models.CASCADE)
    date = models.DateTimeField("跟进日期", auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    def __str__(self):
        return str(self.customer) + str(self.consultant)

    class Meta:
        verbose_name = "跟进记录表"
        verbose_name_plural = "跟进记录表"


class Enrollment(models.Model):
    """
    报名表
    """
    customer = models.ForeignKey('Customer', verbose_name='客户名称', on_delete=models.CASCADE)
    why_us = models.TextField("为什么报名", max_length=1024, default=None, blank=True, null=True)
    your_expectation = models.TextField("学完想达到的具体期望", max_length=1024, blank=True, null=True)
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name="报名日期")
    memo = models.TextField('备注', blank=True, null=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    school = models.ForeignKey('Campuses', on_delete=models.CASCADE)
    enrolment_class = models.ForeignKey("Klass", verbose_name="所报班级", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "报名"
        verbose_name_plural = "报名"
        unique_together = ('enrolment_class', 'customer')

    def __str__(self):
        return str(self.customer)


#########################  学员管理系统   ###########################################

class Klass(models.Model):
    """
    班级表
    """
    campuses = models.ForeignKey('Campuses', verbose_name="校区", on_delete=models.CASCADE)
    course = models.CharField("课程名称", max_length=64, choices=course_choices)
    semester = models.IntegerField("学期")
    price = models.IntegerField("学费", default=20000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField("结业日期", blank=True, null=True)
    teachers = models.ManyToManyField('UserInfo', verbose_name="老师")
    class_type = models.CharField(choices=class_type_choices, max_length=64, verbose_name='班额及类型', blank=True,
                                  null=True)

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'
        unique_together = ("course", "semester", 'campuses')

    def __str__(self):
        return "{}{}({})".format(self.get_course_display(), self.semester, self.campuses)


class Student(models.Model):
    """
    学生表（已报名）
    """
    customer = models.OneToOneField(verbose_name='客户信息', to='Customer', on_delete=models.CASCADE)
    class_list = models.ManyToManyField(verbose_name="已报班级", to='Klass', blank=True)

    emergency_contract = models.CharField(max_length=32, blank=True, null=True, verbose_name='紧急联系人')
    company = models.CharField(verbose_name='公司', max_length=128, blank=True, null=True)
    location = models.CharField(max_length=64, verbose_name='所在区域', blank=True, null=True)
    position = models.CharField(verbose_name='岗位', max_length=64, blank=True, null=True)
    salary = models.IntegerField(verbose_name='薪资', blank=True, null=True)
    welfare = models.CharField(verbose_name='福利', max_length=256, blank=True, null=True)
    date = models.DateField(verbose_name='入职时间', help_text='格式yyyy-mm-dd', blank=True, null=True)
    memo = models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)

    def __str__(self):
        return self.customer.name

    class Meta:
        verbose_name = "学生表"
        verbose_name_plural = "学生表"


class ClassStudyRecord(models.Model):
    """
    班级学习记录
    """
    class_obj = models.ForeignKey(verbose_name="班级", to="Klass", on_delete=models.CASCADE)
    day_num = models.IntegerField(verbose_name="节次", help_text=u"此处填写第几节课或第几天课程...,必须为数字")
    teacher = models.ForeignKey(verbose_name="讲师", to='UserInfo', limit_choices_to={"depart_id": 1002},
                                on_delete=models.CASCADE)
    date = models.DateField(verbose_name="上课日期", auto_now_add=True)

    course_title = models.CharField(verbose_name='本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField(verbose_name='本节课程内容概要', blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField(verbose_name='本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField(verbose_name='作业描述', max_length=500, blank=True, null=True)
    exam = models.TextField(verbose_name='踩分点', max_length=300, blank=True, null=True)

    def __str__(self):
        return "{0} day{1}".format(self.class_obj, self.day_num)

    class Meta:
        verbose_name = "班级学习记录"
        verbose_name_plural = "班级学习记录"


class StudentStudyRecord(models.Model):
    '''
    学生学习记录
    '''
    class_study_record = models.ForeignKey(verbose_name="第几天课程", to="ClassStudyRecord", on_delete=models.CASCADE)
    student = models.ForeignKey(verbose_name="学员", to='Student', on_delete=models.CASCADE)

    record = models.CharField("上课纪录", choices=record_choices, default="checked", max_length=64)

    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(verbose_name='作业评语', max_length=255, blank=True, null=True)
    note = models.CharField(verbose_name="备注", max_length=255, blank=True, null=True)

    homework = models.FileField(verbose_name='作业文件', blank=True, null=True, default=None)
    stu_memo = models.TextField(verbose_name='学员备注', blank=True, null=True)
    date = models.DateTimeField(verbose_name='提交作业日期', auto_now_add=True)

    def __str__(self):
        return "{0}-{1}".format(self.class_study_record, self.student)

    class Meta:
        verbose_name = "学生学习记录"
        verbose_name_plural = "学生学习记录"


#########################  会议室预订   ###########################################


class Room(models.Model):
    """
    会议室表
    """
    caption = models.CharField(max_length=32)
    num = models.IntegerField()

    def __str__(self):
        return self.caption


class Book(models.Model):
    """
    会议室预定信息
    """
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    date = models.DateField()
    time_choices = (
        (1, '8:00'),
        (2, '9:00'),
        (3, '10:00'),
        (4, '11:00'),
        (5, '12:00'),
        (6, '13:00'),
        (7, '14:00'),
        (8, '15:00'),
        (9, '16:00'),
        (10, '17:00'),
        (11, '18:00'),
        (12, '19:00'),
        (13, '20:00'),
    )
    time_id = models.IntegerField(choices=time_choices)

    class Meta:
        unique_together = (
            ('room', 'date', 'time_id'),
        )

    def __str__(self):
        return str(self.user) + "预定了" + str(self.room)
