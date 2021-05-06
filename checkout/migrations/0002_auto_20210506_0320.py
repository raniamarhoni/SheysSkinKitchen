# Generated by Django 3.1.8 on 2021-05-06 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210504_1843'),
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlineitem',
            name='product_size',
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.size'),
        ),
    ]
