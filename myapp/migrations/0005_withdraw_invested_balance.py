# Generated by Django 4.0.5 on 2022-06-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_withdraw_plantype'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdraw',
            name='invested_balance',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
