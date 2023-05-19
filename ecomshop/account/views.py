from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, OTPForm, OTPVerificationForm
from .models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from twilio.rest import Client
import random
from user_profile.views import PreUrl


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('account:user_signin')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('account:user_signin')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user.first_name}, please go to you email {to_email} inbox and click on \
                    received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def register(request):
    global user
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password,
                phone_number=phone_number)
            user.save()
            activateEmail(request, user, email)
            return redirect('account:user_signin')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def login_user(request):
    dest = request.META.get('HTTP_REFERER')
    email = request.session.get('email')
    if email:
        print(email, 'hellow')
        return redirect("homelog:home")
    if request.method == 'POST':
        email = request.POST['singin-email']
        password = request.POST['singin-password']
        print(email)
        print(password)
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            request.session['email'] = email
            next = PreUrl.url
            return redirect(next)
            # return redirect('homelog:home')
        else:
            messages.error(request, "email or password is incorrect!!")
            return redirect('account:user_signin')
    PreUrl(dest)
    return render(request, "signin.html")


def user_signout(request):
    if request.user.is_authenticated:
        logout(request)
        request.session.flush()
    return redirect('homelog:home')


def send_otp(phone_number):
    # Generate a 6-digit OTP
    otp = random.randint(0000, 9999)

    # Set up the Twilio client
    account_sid = 'AC4c969153b5399b72bb17e202f5a2c25f'
    auth_token = '9b35d5558ba27786961c5c3a04e470e7'
    client = Client(account_sid, auth_token)

    # Send the OTP via SMS
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_='+15074317698',
        to=phone_number
    )

    return otp


def login_otp(request):
    if request.session.get('email'):
        return redirect("homelog:home")
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            # country_code = form.cleaned_data['country_code']
            full_phone_number = str('+') + str(91) + phone_number
            print(full_phone_number)
            request.session['phone_number'] = phone_number

            # Send the OTP
            otp = send_otp(full_phone_number)
            print(otp, 'send otp')
            request.session['otp'] = otp

            # Render the OTP verification form
            form = OTPVerificationForm()

            context = {
                'form': form,
            }
            return render(request, 'signin_otp_submit.html', context)
    else:
        form = OTPForm()

    context = {
        'form': form,
    }
    return render(request, 'signin_otp.html', context)


def verify_otp(request):
    print("heidbdnfbdnd sfbdfndg dndgndgnd dfndfsnfsd dfdndg")
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            # Verify the OTP
            if str(otp) == str(request.session['otp']):
                phone_number = request.session['phone_number']

                # Authenticate and log in the user
                user = authenticate(phone_number=phone_number)

                if user is not None:
                    login(request, user)
                    messages.success(request, "You have been logged in!")
                    return redirect('homelog:home')
                else:
                    messages.error(request, "Something went wrong!")
            else:
                messages.error(request, "Invalid OTP!")
    else:
        form = OTPVerificationForm()

    context = {
        'form': form,
    }
    return render(request, 'signin_otp_submit.html', context)
