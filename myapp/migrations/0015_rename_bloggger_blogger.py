# Generated by Django 4.1.7 on 2023-12-06 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_bloggger_options_blog'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bloggger',
            new_name='Blogger',
        ),
    ]