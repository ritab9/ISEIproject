# Generated by Django 3.1.3 on 2020-12-27 22:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20201227_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('CEUs', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('clock_Hours', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('pages', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('summary', models.CharField(help_text='Summarize what you have learned from the combined activities and how you plan to apply this learning to your classroom', max_length=3000, validators=[django.core.validators.MinLengthValidator(1)])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.activitydescription')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.teacher')),
            ],
        ),
        migrations.RemoveField(
            model_name='activityrecord',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='ActivityInstance',
        ),
        migrations.DeleteModel(
            name='ActivityRecord',
        ),
    ]
