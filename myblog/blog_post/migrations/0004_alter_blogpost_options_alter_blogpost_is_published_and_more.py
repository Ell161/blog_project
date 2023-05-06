# Generated by Django 4.2 on 2023-04-30 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0003_alter_blogpost_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='text',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='timestamp',
            field=models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
    ]