# Generated by Django 3.1.3 on 2020-12-29 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20201228_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='current_certification',
            new_name='currentcertification',
        ),
    ]
