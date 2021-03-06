# Generated by Django 4.0.5 on 2022-06-30 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0002_auto_20220630_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegularUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_value', models.FloatField()),
                ('final_value', models.FloatField()),
                ('transaction_date_time', models.DateTimeField(auto_now_add=True)),
                ('percent', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('made_by', models.CharField(blank=True, max_length=100, null=True)),
                ('plantype', models.CharField(choices=[('fixed', 'FIXED'), ('flexible', 'FLEXIBLE')], default='flexible', max_length=200)),
                ('fixed_rate', models.CharField(default='3', max_length=3, null=True)),
                ('made_on', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('present_amount', models.IntegerField(blank=True, null=True)),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('checksum', models.CharField(blank=True, max_length=200, null=True)),
                ('txn_id', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_mode', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('gateway_name', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_txn_id', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('response_message', models.CharField(blank=True, max_length=250, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_by', models.CharField(blank=True, max_length=100, null=True)),
                ('requested_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.IntegerField()),
                ('present_balance', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=5, null=True)),
                ('status_updated_by', models.CharField(blank=True, max_length=100, null=True)),
                ('user_commission', models.IntegerField(blank=True, default=25, null=True)),
                ('status_updated_on', models.DateTimeField(blank=True, null=True)),
                ('plantype', models.CharField(choices=[('fixed', 'FIXED'), ('flexible', 'FLEXIBLE')], default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plantype', models.CharField(choices=[('fixed', 'FIXED'), ('flexible', 'FLEXIBLE')], default='flexible', max_length=200)),
                ('user_commission', models.CharField(default='25', max_length=3)),
                ('fixed_rate', models.CharField(default='0', max_length=3, null=True)),
                ('profession', models.CharField(default='', max_length=200)),
                ('mobile', models.CharField(default='', max_length=10)),
                ('profilephoto', models.ImageField(default='images/profile.png', upload_to='userprofile/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
