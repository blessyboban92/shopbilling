# Generated by Django 3.2.20 on 2023-09-21 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partyapp', '0004_alter_saleitem_mrp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleitem',
            name='purchasetax',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='totalqty',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='unit',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
