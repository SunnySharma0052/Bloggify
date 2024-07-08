from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from random import randint
from django.conf import settings

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        if not User.objects.filter(email_id=request.POST['emailid']).exists():
            new_user = User()
            new_user.first_name = request.POST['firstname']
            new_user.last_name = request.POST['lastname']
            new_user.email_id = request.POST['emailid']
            new_user.password = make_password(request.POST['password'])   
            new_user.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'error_message': "User is already registered"})
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        if User.objects.filter(email_id=request.POST['emailid']).exists():
            user = User.objects.get(email_id=request.POST['emailid'])
            if check_password(request.POST['password'], user.password):
                request.session['is_authenticated'] = True
                request.session['email_id'] = request.POST['emailid']
                request.session['first_name'] = user.first_name
                return redirect('home')
            else:
                return render(request, 'login.html', {'error_message': "Incorrect email id or password"})
        else:
            return render(request, 'login.html', {'error_message': "Incorrect email id or password"})    
    else:
        return render(request, 'login.html')

def profile_view(request):
    if request.session['is_authenticated']:
        return render(request, 'profile.html', 
        {'user': User.objects.get(email_id=request.session['email_id'])})
    else:
        return redirect('login')

def edit_profile_view(request):
    if request.session['is_authenticated']:
        if request.method == 'POST':
            user = User.objects.get(email_id=request.session['email_id'])
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.email_id = request.POST['emailid']
            if 'profilepic' in request.FILES:
                user.image = request.FILES['profilepic']
            user.save()
            request.session['email_id'] = request.POST['emailid']
            return redirect('profile')
        else:
            return render(request, 'editprofile.html', 
            {'user': User.objects.get(email_id=request.session['email_id'])})
    else:
        return redirect('login')

def change_password_view(request):
    if request.session['is_authenticated']:
        if request.method == 'POST':
            user = User.objects.get(email_id=request.session['email_id'])
            if check_password(request.POST['old-password'], user.password):
                if request.POST['new-password'] == request.POST['confirm-password']:
                    user.password = make_password(request.POST['new-password'])
                    user.save()
                    return render(request, 'ChangePassword.html', {'success_message': "Password is changed successfully"})         
                else:
                    return render(request, 'ChangePassword.html', {'error_message': "New and Confirm Passwords mismatched"})         
            else:
                return render(request, 'ChangePassword.html', {'error_message': "Incorrect Old Password"})     
        else:
            return render(request, 'ChangePassword.html') 
    else:
        return redirect('login')

def logout_view(request):
    if request.session['is_authenticated']:
        request.session['is_authenticated'] = False
        request.session['email_id'] = None
        return redirect('login')
    else:
        return redirect('login')

def reset_password_view(request):
    if request.method == 'POST':
        if 'new-password' in request.POST:
            new_password = request.POST['new-password']
            confirm_password = request.POST['confirm-password']
            user = User.objects.get(id=request.POST['user-id'])
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                return render(request, 'resetpassword.html', {'OTP_Status': 'verified', 'User_Id': user.id,
                'success_message': 'Password is reset successfully'})
            else:
                return render(request, 'resetpassword.html', {'OTP_Status': 'verified', 'User_Id': user.id,
                'error_message': 'New and confirm passwords mismatched'})
        elif 'otp' in request.POST:
            user = User.objects.get(id=request.POST['user-id'])
            otp = request.POST['otp']
            if user.password_reset_code == otp:
                return render(request, 'resetpassword.html', {'OTP_Status': 'verified', 'User_Id': user.id,
                'success_message': 'OTP is verified'})
            else:
                return render(request, 'resetpassword.html', {'OTP_Status': 'generated', 'User_Id': user.id,
                'error_message': 'Incorrect OTP '})
        else:
            if User.objects.filter(email_id = request.POST['email-id']).exists():
                user = User.objects.get(email_id = request.POST['email-id'])                
                otp = str(randint(100000, 999999))
                user.password_reset_code = otp
                user.save()
                subject = 'One Time Password(OTP) to reset your password'
                message = "Your OTP to reset your password: " + otp
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email-id']]
                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                except Exception:
                    return render(request, 'resetpassword.html', {'error_message': 'Something went wrong. Please try again'})
                else:
                    return render(request, 'resetpassword.html', {'OTP_Status': 'generated', 'User_Id': user.id,
                    'success_message': 'OTP is mailed successfully to your registered email id'})
            else:
                return render(request, 'resetpassword.html', {'error_message': 'Please enter registered email id'})
    else:
        return render(request, 'ResetPassword.html')
