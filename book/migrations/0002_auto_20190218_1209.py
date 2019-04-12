# Generated by Django 2.0.1 on 2019-02-18 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': '作者'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': '书籍'},
        ),
        migrations.AlterModelOptions(
            name='publish',
            options={'verbose_name': '出版社'},
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to='book.Author', verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Publish', verbose_name='出版社'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=32, verbose_name='名称'),
        ),
    ]
