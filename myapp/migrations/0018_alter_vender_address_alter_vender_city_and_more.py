# Generated by Django 4.1.7 on 2023-12-07 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_blog_user_alter_blogger_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vender',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vender',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vender',
            name='profile_pic',
            field=models.ImageField(blank=True, default='', null=True, upload_to='user_profile'),
        ),
    ]