# Generated by Django 4.0.5 on 2022-06-30 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdraw',
            name='plantype',
            field=models.CharField(blank=True, choices=[('fixed', 'FIXED'), ('flexible', 'FLEXIBLE')], default='', max_length=200, null=True),
        ),
    ]