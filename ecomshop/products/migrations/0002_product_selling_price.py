# Generated by Django 4.1.5 on 2023-05-11 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]