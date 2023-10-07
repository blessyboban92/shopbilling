# Generated by Django 3.2.20 on 2023-09-25 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partyapp', '0009_salepayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='salemodel',
            name='grandtotal',
            field=models.DecimalField(decimal_places=2, default=23.67, max_digits=10),
            preserve_default=False,
        ),
    ]
