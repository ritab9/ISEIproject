# Generated by Django 3.1.3 on 2020-12-14 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201212_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityinstance',
            name='CEUs',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
