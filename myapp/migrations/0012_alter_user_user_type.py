# Generated by Django 4.1.7 on 2023-12-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_product_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Bloger', 'BLOGER'), ('2', 'Vender'), ('3', 'AddUser'), ('1', 'Superuser')], default='1', max_length=10),
        ),
    ]