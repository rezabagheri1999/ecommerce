# Generated by Django 5.2.2 on 2025-06-11 13:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0010_remove_product_rate_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(choices=[(0.5, '0.5'), (1.0, '1.0'), (1.5, '1.5'), (2.0, '2.0'), (2.5, '2.5'), (3.0, '3.0'), (3.5, '3.5'), (4.0, '4.0'), (4.5, '4.5'), (5.0, '5.0')], validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
