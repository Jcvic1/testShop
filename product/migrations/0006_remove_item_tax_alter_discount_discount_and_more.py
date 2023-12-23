# Generated by Django 4.2.8 on 2023-12-21 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_discount_discount_alter_tax_tax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='tax',
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount',
            field=models.FloatField(),
        ),
        migrations.RemoveField(
            model_name='item',
            name='discount',
        ),
        migrations.AlterField(
            model_name='tax',
            name='tax',
            field=models.FloatField(),
        ),
        migrations.AddField(
            model_name='item',
            name='discount',
            field=models.FloatField(null=True),
        ),
    ]
