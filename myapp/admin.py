from django.contrib import admin
from .models import UserProfile,RegularUpdate,Transaction,Withdraw


admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(RegularUpdate)
admin.site.register(Withdraw)
