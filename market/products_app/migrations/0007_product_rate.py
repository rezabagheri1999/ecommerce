# Generated by Django 5.2.2 on 2025-06-11 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0006_product_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=1, null=True),
        ),
    ]
