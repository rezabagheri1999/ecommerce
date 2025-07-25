# Generated by Django 5.2.2 on 2025-06-21 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0013_remove_product_rating_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='available_colors',
        ),
        migrations.AddField(
            model_name='product',
            name='available_colors',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products_app.productcolor'),
            preserve_default=False,
        ),
    ]
