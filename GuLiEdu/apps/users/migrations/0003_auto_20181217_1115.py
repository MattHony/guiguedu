# Generated by Django 2.1.2 on 2018-12-17 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_is_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifycode',
            name='send_type',
            field=models.IntegerField(choices=[(1, 'register'), (2, 'forget'), (3, 'change')], verbose_name='验证类型'),
        ),
    ]
