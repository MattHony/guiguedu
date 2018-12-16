from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import HttpResponse

from users.models import UserProfile
from .forms import UserRegisterForm
from .forms import UserLoginForm

# Create your views here.


def index(request):
    return render(request, 'index.html')


def user_register(request):
    if request.method == 'GET':
        # 引入form类,只是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'register.html', {
            'user_register_form': user_register_form
        })
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']

            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'register.html', {
                    'msg': '用户已经存在',
                })
            else:
                a = UserProfile()
                a.username = email
                a.set_password(password)
                a.email = email
                a.save()
                return redirect(reverse('index'))
        else:
            return render(request, 'register.html', {
                'user_register_form': user_register_form
            })


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user:
                if user.is_start:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return HttpResponse('请前往您的邮箱进行激活,否则无法登录')
            else:
                return render(request, 'login.html', {
                    'msg': '邮箱或密码错误'
                })
        else:
            return render(request, 'login.html', {
                'user_login_form': user_login_form
            })


def user_logout(request):
    # if request.method == 'GET':
    # return render(request, 'logout.html')
    logout(request)
    return redirect(reverse('index'))