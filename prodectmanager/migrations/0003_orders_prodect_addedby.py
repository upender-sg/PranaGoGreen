# Generated by Django 3.1.5 on 2021-04-05 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodectmanager', '0002_orderprodects_prodect_addedby'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='prodect_addedby',
            field=models.CharField(default='', max_length=10),
        ),
    ]
