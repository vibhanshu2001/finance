from django.shortcuts import render,redirect
from .forms import ExtendedUserCreationForm, UserProfileForm, RegularUpdateForm, WithdrawForm
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings
import json
import requests
from . import Checksum
from django.http import HttpResponse
from .models import UserProfile, RegularUpdate, Transaction, Withdraw
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
import pyrebase
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from io import StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from html import escape
import io

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = context_dict
    html  = template.render(context)
    result = io.BytesIO()

    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def pdf_all_transactions(request):
    results = Transaction.objects.all()
    return render_to_pdf(
            'pdf-all-transactions.html',
            {
                'pagesize':'A4',
                'mylist': results,
            }
        )
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the email address you registered with, and check your spam folder."
    success_url = reverse_lazy('password_reset_done')

def password_reset_done(request):
    data = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the email address you registered with, and check your spam folder."
    return render(request, 'password-reset-mail_sent.html',{'data':data})

@login_required
def withdraw(request):
    data = Withdraw.objects.all()
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.save()
            return redirect('/withdraw')
    form = WithdrawForm(initial={'requested_by': request.user.username})
    return render(request, 'withdraw.html',{'form':form,'data':data})
@login_required
def admin_withdrawal_requests(request):
    data = Withdraw.objects.all()
    return render(request, 'admin-templates/admin-withdrawal-requests.html',{'data':data})
@login_required
def fixed_rate_update(request):
    result = Transaction.objects.all()
    for i in result:
        if i.plantype == 'fixed' and i.status == 'TXN_SUCCESS':
            percent_alter = int(i.fixed_rate)
            print(i.present_amount)
            i.present_amount =  i.present_amount + i.amount*percent_alter/100
            i.last_updated = timezone.now()
            i.save()
            
    return redirect('admin_home')

@login_required
def fixed_rate_page(request):
    return render(request,'admin-templates/fixed-rate-update.html')
    
@login_required
def index(request):
    data = Transaction.objects.all()
    return render(request,'index.html',{'data':data})
@login_required
def regular_update(request):
    reg_update = RegularUpdate.objects.all()
    if request.method == 'POST':
        form = RegularUpdateForm(request.POST)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.save()
            result = Transaction.objects.all()
            for i in result:
                if i.plantype == 'flexible' and i.status == 'TXN_SUCCESS':
                    myvar = RegularUpdate.objects.last()
                    percent_alter = myvar.percent
                    i.present_amount =  i.present_amount + i.amount*percent_alter/100
                    i.last_updated = myvar.transaction_date_time
                    i.save()
            return redirect('/regular-update')
    form = RegularUpdateForm()
    return render(request,'admin-templates/regular-update.html',{'form':form,'reg_update':reg_update})
def admin_home(request):
    transaction = Transaction.objects.all()
    result = Transaction.objects.all()
    total_money=0
    total_present_value = 0
    for i in transaction:
        if i.status == 'TXN_SUCCESS':
            total_money += i.amount
            total_present_value += i.present_amount
        userdata = UserProfile.objects.all()
        for j in userdata:
            if j.user == i.made_by:
                i.plantype = j.plantype
                i.save()
    
    return render(request,'admin-templates/admin-home.html',{'total_money':total_money,'result':result,'total_present_value':total_present_value})
def admin_all_transactions(request):
    transaction = Transaction.objects.all()
    return render(request,'admin-templates/admin-all-transaction.html',{'transaction':transaction})
def admin_all_users(request):
    users = User.objects.all()
    userprofile = UserProfile.objects.all()
    return render(request,'admin-templates/all-users.html',{'userprofile':userprofile})

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')

    return render(request, 'login.html')
def handleLogout(request):
    logout(request)
    return redirect('login')
def signUp(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST, request.FILES)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('admin_home')
    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()
    context = {'form': form,'profile_form':profile_form}
    return render(request, 'admin-templates/signup.html',context)
useramount=0
@login_required
def payment(request):
    if request.method == "GET":
        return render(request, 'payment.html')
    try:
        useramount = int(request.POST['amount'])
    except:
        return render(request, 'payment.html', context={'error': 'Wrong Accound Details or amount'})
    MERCHANT_KEY = settings.PAYTM_SECRET_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL
    order_id = Checksum.__id_generator__()
    amount = useramount
    if amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':str(order_id),
                    'TXN_AMOUNT': str(amount),
                    'CUST_ID':'v2001.garg@gmail.com',
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':'http://127.0.0.1:8000/response/',
                }
        param_dict = data_dict
        checksum = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        param_dict['CHECKSUMHASH'] = checksum
        transaction = Transaction.objects.create(made_by=request.user, amount=amount,present_amount=amount)
        transaction.save()
        transaction.checksum = checksum
        transaction.order_id = order_id
        transaction.save()
        return render(request,"redirect.html",{'paytmdict':param_dict})
    return HttpResponse("Invalid Request")
@csrf_exempt
def response(request):
    order = None
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] =form[i]
        if i == 'ORDERID':
            order = Transaction.objects.get(order_id=form[i])

    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_SECRET_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]

        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            order.txn_id = data_dict['TXNID']
            order.payment_mode = data_dict['PAYMENTMODE']
            order.status = data_dict['STATUS']
            order.gateway_name = data_dict['GATEWAYNAME']
            order.bank_txn_id = data_dict['BANKTXNID']
            order.bank_name = data_dict['BANKNAME']
            order.response_message = data_dict['RESPMSG']
            order.save()
            # 
            result = Transaction.objects.all()
            for i in result:
                userdata = UserProfile.objects.all()
                for j in userdata:
                    if j.user == i.made_by:
                        i.plantype = j.plantype
                        i.fixed_rate = j.fixed_rate
                        i.save()
                # reg_update = RegularUpdate.objects.last()
                # percent_alter = reg_update.percent
                # i.present_amount =  i.present_amount + i.amount*percent_alter/100
                # i.save()
                    
            # 
            return redirect('/')
            # return render(request,"index.html")
            # return render(request,"response.html",{"paytm":data_dict})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)
