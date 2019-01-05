from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import HttpResponse

from users.models import UserProfile, EmailVerifyCode
from .forms import UserForgetForm, UserChangeImageForm, UserChangeEmailForm
from .forms import UserRegisterForm
from .forms import UserLoginForm
from .forms import UserResetForm
from .forms import UserChangeInfoForm

from tools.send_email_tool import send_email_code

# Create your views here.


def index(request):
    return render(request, 'index.html')


def user_register(request):
    if request.method == 'GET':
        # 引入form类,只是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'users/register.html', {
            'user_register_form': user_register_form
        })
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']

            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'users/register.html', {
                    'msg': '用户已经存在',
                })
            else:
                a = UserProfile()
                a.username = email
                a.set_password(password)
                a.email = email
                a.save()
                # 激活邮箱
                send_email_code(email, 1)
                return HttpResponse('请尽快前往您的邮箱进行激活,否则无法登录')
                # return redirect(reverse('index'))
        else:
            return render(request, 'users/register.html', {
                'user_register_form': user_register_form
            })


def user_login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
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
                return render(request, 'users/login.html', {
                    'msg': '邮箱或密码错误'
                })
        else:
            return render(request, 'users/login.html', {
                'user_login_form': user_login_form
            })


def user_logout(request):
    # if request.method == 'GET':
    # return render(request, 'logout.html')
    logout(request)
    return redirect(reverse('index'))


def user_active(request, code):
    if code:
        email_ver_list = EmailVerifyCode.objects.filter(code=code)
        if email_ver_list:
            email_ver = email_ver_list[0]
            email = email_ver.email
            user_list = UserProfile.objects.filter(username=email)
            if user_list:
                user = user_list[0]
                user.is_start = True
                user.save()
                return redirect(reverse('users:user_login'))
            else:
                pass
        else:
            pass
    else:
        pass


def user_forget(request):
    if request.method == 'GET':
        user_forget_form = UserForgetForm()
        return render(request, 'users/forgetpwd.html', {
            'user_forget_form': user_forget_form
        })
    else:
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email = user_forget_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(email=email)
            if user_list:
                send_email_code(email, 2)
                return HttpResponse('请尽快去您的邮箱重置密码')
            else:
                return render(request, 'users/forgetpwd.html', {
                    'msg': '用户不存在'
                })
        else:
            return render(request, 'users/forgetpwd.html', {
                'user_forget_form': user_forget_form
            })


# 忘记密码 传入code参数 多次使用验证码进行验证
def user_reset(request, code):
    if code:
        if request.method == 'GET':
            return render(request, 'users/password_reset.html', {
                'code': code
            })
        else:
            user_reset_form = UserResetForm(request.POST)
            if user_reset_form.is_valid():
                password = user_reset_form.cleaned_data['password']
                password1 = user_reset_form.cleaned_data['password1']
                if password == password1:
                    email_ver_list = EmailVerifyCode.objects.filter(code=code)
                    if email_ver_list:
                        email_ver = email_ver_list[0]
                        email = email_ver.email
                        user_list = UserProfile.objects.filter(email=email)
                        if user_list:
                            user = user_list[0]
                            user.set_password(password1)
                            user.save()
                            return redirect(reverse('users:user_login'))
                        else:
                            pass
                    else:
                        pass
                else:
                    return render(request, 'users/password_reset.html', {
                        'msg': '两次密码不一致',
                        'code': code
                    })
            else:
                return render(request, 'users/password_reset.html', {
                    'user_reset_form': user_reset_form,
                    'code': code
                })


def user_info(request):
    return render(request, 'users/usercenter_info.html')


def user_changeimage(request):
    # instance 用做对request.user修改 指明实例对象
    user_changeimage_form = UserChangeImageForm(request.POST, request.FILES, instance=request.user)
    if user_changeimage_form.is_valid():
        user_changeimage_form.save(commit=True)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'failed'})


def user_changeinfo(request):
    user_changeinfo_form = UserChangeInfoForm(request.POST, request.FILES, instance=request.user)
    if user_changeinfo_form.is_valid():
        user_changeinfo_form.save(commit=True)
        return JsonResponse({'status': 'ok', 'msg': '修改成功'})
    else:
        return JsonResponse({'status': 'failed', 'msg': '修改失败'})


def user_changeemail(request):
    """
    func: 功能 参数 返回值 当用户修改邮箱,点击获取验证码时,通过这个函数处理,获取验证码
    :param request: http请求对象
    :return: 返回json数据.在模板页面进行处理
    """
    user_changeemail_form = UserChangeEmailForm(request.POST)
    if user_changeemail_form.is_valid():
        email = user_changeemail_form.cleaned_data['email']
        user_list = UserProfile.objects.filter(Q(email=email)|Q(username=email))
        if user_list:
            return JsonResponse({'status': 'failed', 'msg': '邮箱已经被绑定'})
        else:
            # 发送邮箱验证码之前,去发送验证码的表中去查找,查看之前是否往这个邮箱发送过此类验证码
            email_ver_list = EmailVerifyCode.objects.filter(email=email, send_type=3)
            if email_ver_list:
                email_ver = email_ver_list.order_by('-add_time')[0]
                # 判断当前时间和最近发送的验证码添加时间之差
                if (datetime.now()-email_ver.add_time).seconds >= 60:
                    send_email_code(email, 3)
                    # 清除之前已经存在的验证码
                    email_ver.delete()
                    return JsonResponse({'status': 'ok', 'msg': '请尽快到邮箱中获取验证码'})
                else:
                    return JsonResponse({'status': 'fail', 'msg': '请不要重复发送验证码'})
            else:
                send_email_code(email, 3)
                return JsonResponse({'status': 'ok', 'msg': '请尽快到邮箱中获取验证码'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '您输入的邮箱有误'})
