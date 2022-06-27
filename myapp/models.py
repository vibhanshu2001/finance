from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
PLAN_TYPE = (
    ('fixed','FIXED'),
    ('flexible', 'FLEXIBLE'),
)
User = get_user_model()
class UserProfile(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    plantype = models.CharField(max_length=200, choices=PLAN_TYPE, default='flexible')
    user_commission = models.CharField(max_length=3, null=False, default='25')
    fixed_rate = models.CharField(max_length=3, null=True, default='0')
    profession = models.CharField(max_length=200, null=False, default='')
    mobile = models.CharField(max_length=10, null=False, default='')
    profilephoto = models.ImageField(upload_to='userprofile/', default='images/profile.png')
    # total_wallet_money = models.CharField(max_length=10, null=False, default='')
    def __str__(self):
        return self.user.username

class RegularUpdate(models.Model):
    initial_value = models.FloatField()
    final_value = models.FloatField()
    transaction_date_time = models.DateTimeField(auto_now_add=True)
    percent = models.FloatField(null=True, blank=True)
    def save(self, *args, **kwargs):
        self.percent = (self.final_value - self.initial_value)*100/self.initial_value
        super(RegularUpdate, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.transaction_date_time)

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    plantype = models.CharField(max_length=200, choices=PLAN_TYPE, default='flexible')
    fixed_rate = models.CharField(max_length=3, null=True, default='3')
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    present_amount = models.IntegerField(null=True, blank=True)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=200, null=True, blank=True)
    txn_id = models.CharField(max_length=100, null=True, blank=True)
    payment_mode = models.CharField(max_length=100, null=True, blank=True,default='')
    status = models.CharField(max_length=100, null=True, blank=True)
    gateway_name = models.CharField(max_length=100, null=True, blank=True)
    bank_txn_id = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    response_message = models.CharField(max_length=250, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.order_id)
class Withdraw(models.Model):
    requested_by = models.CharField(max_length=100, null=True, blank=True)
    requested_on = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField()
    def __str__(self):
        return str(self.requested_by)