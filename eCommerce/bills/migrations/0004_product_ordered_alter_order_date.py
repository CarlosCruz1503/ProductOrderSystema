# Generated by Django 4.1.7 on 2023-03-24 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0003_rename_product_orderdetail_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ordered',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
