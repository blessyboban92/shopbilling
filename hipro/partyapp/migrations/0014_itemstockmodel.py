# Generated by Django 3.2.20 on 2023-10-06 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiapp', '0010_itempricelistmaster_itemid1'),
        ('partyapp', '0013_salecounter'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemStockModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('TotalCount', models.IntegerField(default=0)),
                ('itemname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hiapp.itemmaster')),
            ],
        ),
    ]
