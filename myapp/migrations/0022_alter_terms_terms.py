# Generated by Django 4.1.7 on 2023-12-12 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_policy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terms',
            name='terms',
            field=models.CharField(max_length=1000),
        ),
    ]
