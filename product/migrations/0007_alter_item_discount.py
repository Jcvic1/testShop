# Generated by Django 4.2.8 on 2023-12-21 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_remove_item_tax_alter_discount_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]
