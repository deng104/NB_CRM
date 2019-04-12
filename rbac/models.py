from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=32, verbose_name='权限名称')
    type = models.CharField(max_length=32, verbose_name='资源类型', choices=[("menu", "菜单权限"), ("link", "链接权限"), ("button", "按钮权限")])
    url = models.CharField(max_length=128, verbose_name='访问url地址', null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, verbose_name='父权限', blank=True)
    pids=models.CharField(max_length=32,null=True,blank=True,verbose_name="父权限组合") # "1/5/13" 可避开递归,当然需要重写save

    class Meta:
        verbose_name_plural = '权限表'
        verbose_name = '权限表'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        pid_list=[]
        parent=self.parent
        while self.parent:
            pid_list.append(self.parent_id)
            self.parent=self.parent.parent
        self.parent=parent
        self.pids = "/".join([str(i) for i in pid_list])
        super(Permission, self).save(*args, **kwargs)


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', verbose_name='角色所拥有的权限', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '角色表'
        verbose_name = '角色表'


class User(models.Model):
    """
    用户表
    """
    roles = models.ManyToManyField(to=Role, verbose_name='用户所拥有的角色', blank=True,null=True)

    class Meta:
        abstract = True
