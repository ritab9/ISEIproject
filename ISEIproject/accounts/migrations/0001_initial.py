# Generated by Django 3.1.3 on 2020-12-11 21:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Describe the possible activities', max_length=100)),
                ('category', models.CharField(choices=[('i', 'Independent'), ('g', 'Group'), ('c', 'Collaboration'), ('p', 'Presentation & Writing')], help_text='Choose a category', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of the school', max_length=50, unique=True)),
                ('abbreviation', models.CharField(default='none', help_text=' Enter the abbreviation for this school', max_length=4)),
                ('principal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.school')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('current_certification', models.CharField(choices=[('v', 'Vocational'), ('d', 'Designated'), ('c', 'Conditional'), ('e', 'Semi Professional'), ('b', 'Basic'), ('s', 'Standard'), ('p', 'Professional')], help_text='Choose a certification', max_length=1)),
                ('summary', models.CharField(help_text='Summarize what you have learned from the combined activities and how you plan to apply this learning to your classroom', max_length=3000, validators=[django.core.validators.MinLengthValidator(200)])),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CEUs', models.DecimalField(decimal_places=2, max_digits=2)),
                ('clock_Hours', models.DecimalField(decimal_places=1, max_digits=3)),
                ('pages', models.DecimalField(decimal_places=0, max_digits=3)),
                ('activityrecord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.activityrecord')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.activitydescription')),
            ],
        ),
    ]