# Generated by Django 3.2.20 on 2023-09-10 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiapp', '0003_alter_itemmaster_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brandname', models.CharField(max_length=30)),
                ('branddescription', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='itemmaster',
            name='unit',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemmaster',
            name='brand',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='hiapp.brandmaster'),
        ),
    ]
