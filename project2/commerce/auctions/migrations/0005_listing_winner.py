# Generated by Django 3.1.4 on 2021-01-17 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_is_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]