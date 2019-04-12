from django.db import models


# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "作者"


class Publish(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "出版社"


class Book(models.Model):
    title = models.CharField(max_length=32, verbose_name="名称")
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="价格")
    publisher = models.ForeignKey(to="Publish", on_delete=models.CASCADE, verbose_name="出版社")
    authors = models.ManyToManyField(to='Author', verbose_name="作者")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "书籍"
