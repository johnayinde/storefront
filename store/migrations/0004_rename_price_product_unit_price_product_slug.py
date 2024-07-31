# Generated by Django 5.0.7 on 2024-07-30 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_customer_store_custo_first_n_a7e990_idx_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='unit_price',
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='-'),
            preserve_default=False,
        ),
    ]
