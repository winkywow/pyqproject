# Generated by Django 2.0.3 on 2018-04-08 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20180408_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sid',
            field=models.CharField(max_length=50, unique=1),
        ),
    ]
