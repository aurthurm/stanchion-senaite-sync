# Generated by Django 2.2a1 on 2019-02-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='fid',
            field=models.CharField(max_length=50, verbose_name='Facility ZW ID'),
        ),
    ]
