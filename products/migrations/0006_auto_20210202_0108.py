# Generated by Django 3.1.5 on 2021-02-02 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210201_2359'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product_Variation',
            new_name='Variation',
        ),
    ]
