# Generated by Django 2.2.4 on 2019-08-10 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0014_products_wished_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='list',
            field=models.ManyToManyField(related_name='products', to='wishlist.List'),
        ),
    ]
