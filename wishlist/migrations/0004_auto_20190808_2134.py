# Generated by Django 2.2.4 on 2019-08-08 18:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0003_auto_20190808_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricehistory',
            name='from_date',
            field=models.DateField(default=datetime.datetime(2019, 8, 8, 18, 34, 0, 253998, tzinfo=utc)),
        ),
    ]
