# Generated by Django 3.2.20 on 2023-09-27 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partyapp', '0012_alter_salemodel_sale_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saleno', models.PositiveIntegerField(default=1)),
            ],
        ),
    ]
