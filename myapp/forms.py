from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,RegularUpdate,Withdraw

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    class Meta:
        model = User
        fields = ('username','email','first_name', 'last_name','password1','password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('plantype','profession','mobile','user_commission','fixed_rate','profilephoto')
class RegularUpdateForm(forms.ModelForm):
    class Meta:
        model = RegularUpdate
        fields = ('initial_value','final_value')
        labels = {
            'initial_value': 'Initial Value',
            'final_value': 'Final Value',
        }
class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ('requested_by','amount','status','status_updated_by','status_updated_on','present_balance','plantype','user_commission','invested_balance')
        labels = {
            'requested_by': 'Requested by',
            'amount': 'Withdrawal Amount',
            'status': 'Status (Type A/R)',
            'status_updated_by': 'Status updated by',
            'present_balance': 'Present Balance',
            'plantype': 'Plantype',
            'user_commission': 'User Commission',
            'invested_balance': 'Invested Balance'
        }
        widgets = {
        'requested_by':forms.TextInput(attrs={'readonly':True}),
        'status_updated_by':forms.TextInput(attrs={'readonly':True}),
        'plantype':forms.TextInput(attrs={'readonly':True}),
        }