from django.shortcuts import render,redirect
from account.forms import CreateUserForm,LoginForm,UpdateUserForm
from django.contrib.auth.models import User

#for email verfication
from django.contrib.sites.shortcuts import get_current_site # 3ashen n5od lsite l2lna
from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payment.models import  ShippingAddress,Order,OrderItem
from payment.forms import ShippingForm





# Create your views here.
def register(request):
    form=CreateUserForm
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.is_active=False
            user.save()

            # Email Verfication setup
            current_site=get_current_site(request) #site lal web l2lna
            subject='Acouunt Verfication Email' # shu badon yb3tolna 3a emailna subject
            message=render_to_string('account/registration/email-verification.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':user_tokenizer_generate.make_token(user),


            })

            user.email_user(subject=subject,message=message)




            return redirect('email-verification-sent') #mn3ml redirect hasab lname

    context={'form':form}
    
    return render(request,'account/registration/register.html',context)


def email_verification(request, uidb64, token):

    # uniqueid

    unique_id = force_str(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=unique_id)
    
    # Success

    if user and user_tokenizer_generate.check_token(user, token): # is kabsna 3al verification

        user.is_active = True

        user.save()

        return redirect('email-verification-success')


    # Failed 

    else:

        return redirect('email-verification-failed')



def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):

    return render(request, 'account/registration/email-verification-success.html')



def email_verification_failed(request):

    return render(request, 'account/registration/email-verification-failed.html')




def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")


    context = {'form':form}

    return render(request, 'account/my-login.html', context=context)




def user_logout(request):

    for key in list(request.session.keys()):# jbna kel lkeys to3ol lsession bas  badna nshil to3ol lshopping cart bas n3ml logout badnash yeha tnm7e lcart w tseer 0 ma b2lba shi
        if key == 'session_key':
            continue
        else:
            del request.session[key]

    messages.success(request,"logout success")# bas n3ml lmessage btbyn bel store 3asehn t7ta redirect bel store bas n7na 7atyneha bel base.html l2no lbase.html b2lb lstore
    return redirect('store')



@login_required(login_url='my-login')
def dashboard(request):
    return render(request,'account/dashboard.html')



@login_required(login_url='my-login')
def profile_managment(request):
    user_form=UpdateUserForm(instance=request.user) #y3ne bnfs the lahza shu b2lba bt5da
    if request.method=='POST':
        user_form=UpdateUserForm(request.POST,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.info(request,"Account Updated")
            return redirect('dashboard')

   

    context={'user_form':user_form}

    return render(request,'account/profile-managment.html',context)


@login_required(login_url='my-login')
def delete_account(request):
    user=User.objects.get(id=request.user.id)
    if request.method=='POST':
        user.delete()
        messages.error(request,"Account Deleted")
        return redirect('store')

    return render(request,'account/delete-account.html')
            



@login_required(login_url='my-login')
def manage_shipping(request):

    try:

        # Account user with shipment information

        shipping = ShippingAddress.objects.get(user=request.user.id)  #mnshufa eza mawjodi linfo bel database


    except ShippingAddress.DoesNotExist:

        # Account user with no shipment information  

        shipping = None  #hon eza mish mawjode


    form = ShippingForm(instance=shipping)


    if request.method == 'POST':

        form = ShippingForm(request.POST, instance=shipping)  #mn5od e5er value 7atynehon lal shipping info

        if form.is_valid():

            # Assign the user FK on the object

            shipping_user = form.save(commit=False)

            # Adding the FK itself

            shipping_user.user = request.user  #eza 3amel login by5od luser foreing key


            shipping_user.save()

            messages.info(request, "Update success!")

            return redirect('dashboard')


    context = {'form':form}

    return render(request, 'account/manage-shipping.html', context=context)




@login_required(login_url='my-login')
def track_orders(request):
    orders=OrderItem.objects.filter(user=request.user)
    try:
        context={'orders':orders}
        return render(request,'account/track-order.html' ,context=context)
    except:
        return render(request,'account/track-order.html')





