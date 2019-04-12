# Generated by Django 2.0.1 on 2019-02-18 14:55

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=32, null=True, unique=True, verbose_name='姓名')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='年龄')),
                ('gender', models.CharField(choices=[('Female', '女'), ('Male', '男')], default='Male', max_length=10, verbose_name='性别')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m', verbose_name='头像')),
            ],
            options={
                'verbose_name': '员工表',
                'verbose_name_plural': '员工表',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_id', models.IntegerField(choices=[(1, '8:00'), (2, '9:00'), (3, '10:00'), (4, '11:00'), (5, '12:00'), (6, '13:00'), (7, '14:00'), (8, '15:00'), (9, '16:00'), (10, '17:00'), (11, '18:00'), (12, '19:00'), (13, '20:00')])),
            ],
        ),
        migrations.CreateModel(
            name='Campuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='校区')),
                ('address', models.CharField(blank=True, max_length=512, null=True, verbose_name='详细地址')),
            ],
            options={
                'verbose_name': '校区',
                'verbose_name_plural': '校区',
            },
        ),
        migrations.CreateModel(
            name='ClassStudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.IntegerField(help_text='此处填写第几节课或第几天课程...,必须为数字', verbose_name='节次')),
                ('date', models.DateField(auto_now_add=True, verbose_name='上课日期')),
                ('course_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节课程标题')),
                ('course_memo', models.TextField(blank=True, null=True, verbose_name='本节课程内容概要')),
                ('has_homework', models.BooleanField(default=True, verbose_name='本节有作业')),
                ('homework_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节作业标题')),
                ('homework_memo', models.TextField(blank=True, max_length=500, null=True, verbose_name='作业描述')),
                ('exam', models.TextField(blank=True, max_length=300, null=True, verbose_name='踩分点')),
            ],
            options={
                'verbose_name': '班级学习记录',
                'verbose_name_plural': '班级学习记录',
            },
        ),
        migrations.CreateModel(
            name='ConsultRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='跟进内容...')),
                ('status', models.CharField(choices=[('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'), ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效')], help_text='选择客户此时的状态', max_length=8, verbose_name='跟进状态')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='跟进日期')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL, verbose_name='跟进人')),
            ],
            options={
                'verbose_name': '跟进记录表',
                'verbose_name_plural': '跟进记录表',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qq', models.CharField(help_text='QQ号必须唯一', max_length=64, unique=True, verbose_name='QQ')),
                ('qq_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='QQ昵称')),
                ('name', models.CharField(blank=True, help_text='学员报名后，请改为真实姓名', max_length=32, null=True, verbose_name='姓名')),
                ('sex', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], default='male', max_length=16, null=True, verbose_name='性别')),
                ('birthday', models.DateField(blank=True, default=None, help_text='格式yyyy-mm-dd', null=True, verbose_name='出生日期')),
                ('phone', models.BigIntegerField(blank=True, null=True, verbose_name='手机号')),
                ('source', models.CharField(choices=[('qq', 'qq群'), ('referral', '内部转介绍'), ('website', '官方网站'), ('baidu_ads', '百度推广'), ('office_direct', '直接上门'), ('WoM', '口碑'), ('public_class', '公开课'), ('website_luffy', '路飞官网'), ('others', '其它')], default='qq', max_length=64, verbose_name='客户来源')),
                ('class_type', models.CharField(choices=[('fulltime', '脱产班'), ('online', '网络班'), ('weekend', '周末班')], default='fulltime', max_length=64, verbose_name='班级类型')),
                ('customer_note', models.TextField(blank=True, null=True, verbose_name='客户备注')),
                ('status', models.CharField(choices=[('signed', '已报名'), ('unregistered', '未报名'), ('studying', '学习中'), ('paid_in_full', '学费已交齐')], default='unregistered', help_text='选择客户此时的状态', max_length=64, verbose_name='状态')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='咨询日期')),
                ('last_consult_date', models.DateField(auto_now_add=True, verbose_name='最后跟进日期')),
                ('deal_date', models.DateTimeField(blank=True, null=True, verbose_name='成交日期')),
            ],
            options={
                'verbose_name': '客户',
                'verbose_name_plural': '客户',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('campuse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Campuses')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('why_us', models.TextField(blank=True, default=None, max_length=1024, null=True, verbose_name='为什么报名')),
                ('your_expectation', models.TextField(blank=True, max_length=1024, null=True, verbose_name='学完想达到的具体期望')),
                ('enrolled_date', models.DateTimeField(auto_now_add=True, verbose_name='报名日期')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='客户名称')),
            ],
            options={
                'verbose_name': '报名',
                'verbose_name_plural': '报名',
            },
        ),
        migrations.CreateModel(
            name='Klass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('Linux', 'Linux中高级'), ('PythonFullStack', 'Python高级全栈开发')], max_length=64, verbose_name='课程名称')),
                ('semester', models.IntegerField(verbose_name='学期')),
                ('price', models.IntegerField(default=20000, verbose_name='学费')),
                ('memo', models.CharField(blank=True, max_length=100, null=True, verbose_name='说明')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('graduate_date', models.DateField(blank=True, null=True, verbose_name='结业日期')),
                ('class_type', models.CharField(blank=True, choices=[('fulltime', '脱产班'), ('online', '网络班'), ('weekend', '周末班')], max_length=64, null=True, verbose_name='班额及类型')),
                ('campuses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Campuses', verbose_name='校区')),
                ('teachers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='老师')),
            ],
            options={
                'verbose_name': '班级',
                'verbose_name_plural': '班级',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emergency_contract', models.CharField(blank=True, max_length=32, null=True, verbose_name='紧急联系人')),
                ('company', models.CharField(blank=True, max_length=128, null=True, verbose_name='公司')),
                ('location', models.CharField(blank=True, max_length=64, null=True, verbose_name='所在区域')),
                ('position', models.CharField(blank=True, max_length=64, null=True, verbose_name='岗位')),
                ('salary', models.IntegerField(blank=True, null=True, verbose_name='薪资')),
                ('welfare', models.CharField(blank=True, max_length=256, null=True, verbose_name='福利')),
                ('date', models.DateField(blank=True, help_text='格式yyyy-mm-dd', null=True, verbose_name='入职时间')),
                ('memo', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('class_list', models.ManyToManyField(blank=True, to='crm.Klass', verbose_name='已报班级')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='客户信息')),
            ],
            options={
                'verbose_name': '学生表',
                'verbose_name_plural': '学生表',
            },
        ),
        migrations.CreateModel(
            name='StudentStudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.CharField(choices=[('checked', '已签到'), ('vacate', '请假'), ('late', '迟到'), ('noshow', '缺勤'), ('leave_early', '早退')], default='checked', max_length=64, verbose_name='上课纪录')),
                ('score', models.IntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'C+'), (50, 'C'), (40, 'C-'), (0, ' D'), (-1, 'N/A'), (-100, 'COPY'), (-1000, 'FAIL')], default=-1, verbose_name='本节成绩')),
                ('homework_note', models.CharField(blank=True, max_length=255, null=True, verbose_name='作业评语')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('homework', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='作业文件')),
                ('stu_memo', models.TextField(blank=True, null=True, verbose_name='学员备注')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='提交作业日期')),
                ('class_study_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ClassStudyRecord', verbose_name='第几天课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Student', verbose_name='学员')),
            ],
            options={
                'verbose_name': '学生学习记录',
                'verbose_name_plural': '学生学习记录',
            },
        ),
        migrations.AddField(
            model_name='enrollment',
            name='enrolment_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Klass', verbose_name='所报班级'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Campuses'),
        ),
        migrations.AddField(
            model_name='customer',
            name='class_list',
            field=models.ManyToManyField(blank=True, to='crm.Klass', verbose_name='已报班级'),
        ),
        migrations.AddField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(blank=True, limit_choices_to={'depart_id': 1}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL, verbose_name='销售'),
        ),
        migrations.AddField(
            model_name='customer',
            name='introduce_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='转介绍自学员'),
        ),
        migrations.AddField(
            model_name='consultrecord',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='所咨询客户'),
        ),
        migrations.AddField(
            model_name='classstudyrecord',
            name='class_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Klass', verbose_name='班级'),
        ),
        migrations.AddField(
            model_name='classstudyrecord',
            name='teacher',
            field=models.ForeignKey(limit_choices_to={'depart_id': 1002}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='讲师'),
        ),
        migrations.AddField(
            model_name='book',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Room'),
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='depart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Department'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='klass',
            unique_together={('course', 'semester', 'campuses')},
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together={('enrolment_class', 'customer')},
        ),
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('room', 'date', 'time_id')},
        ),
    ]
