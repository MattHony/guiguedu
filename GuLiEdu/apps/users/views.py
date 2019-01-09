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
from django.views.generic import View

from courses.models import CourseInfo
from operations.models import UserLove, UserMessage
from orgs.models import OrgInfo, TeacherInfo
from users.models import UserProfile, EmailVerifyCode, BannerInfo
from .forms import UserForgetForm, UserChangeImageForm, UserChangeEmailForm
from .forms import UserRegisterForm
from .forms import UserLoginForm
from .forms import UserResetForm, UserResetEmailForm
from .forms import UserChangeInfoForm

from tools.send_email_tool import send_email_code

# Create your views here.


class IndexView(View):
    def get(self, request):
        all_banners = BannerInfo.objects.all().order_by('-add_time')[:5]
        banner_courses = CourseInfo.objects.filter(is_banner=True)[:3]
        all_courses = CourseInfo.objects.filter(is_banner=True)[:6]
        all_orgs = OrgInfo.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'banner_courses': banner_courses,
            'all_courses': all_courses,
            'all_orgs': all_orgs,
        })

# def index(request):
#     all_banners = BannerInfo.objects.all().order_by('-add_time')[:5]
#     banner_courses = CourseInfo.objects.filter(is_banner=True)[:3]
#     all_courses = CourseInfo.objects.filter(is_banner=True)[:6]
#     all_orgs = OrgInfo.objects.all()[:15]
#     return render(request, 'index.html', {
#         'all_banners': all_banners,
#         'banner_courses': banner_courses,
#         'all_courses': all_courses,
#         'all_orgs': all_orgs,
#     })


class UserRegisterView(View):
    def get(self, request):
        # 引入form类,只是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'users/register.html', {
            'user_register_form': user_register_form
        })

    def post(self, request):
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
# def user_register(request):
#     if request.method == 'GET':
#         # 引入form类,只是为了使用验证码
#         user_register_form = UserRegisterForm()
#         return render(request, 'users/register.html', {
#             'user_register_form': user_register_form
#         })
#     else:
#         user_register_form = UserRegisterForm(request.POST)
#         if user_register_form.is_valid():
#             email = user_register_form.cleaned_data['email']
#             password = user_register_form.cleaned_data['password']
#
#             user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
#             if user_list:
#                 return render(request, 'users/register.html', {
#                     'msg': '用户已经存在',
#                 })
#             else:
#                 a = UserProfile()
#                 a.username = email
#                 a.set_password(password)
#                 a.email = email
#                 a.save()
#                 # 激活邮箱
#                 send_email_code(email, 1)
#                 return HttpResponse('请尽快前往您的邮箱进行激活,否则无法登录')
#                 # return redirect(reverse('index'))
#         else:
#             return render(request, 'users/register.html', {
#                 'user_register_form': user_register_form
#             })


class UserLoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user:
                if user.is_start:
                    login(request, user)
                    # 当登录成功,刷新一条消息
                    a = UserMessage()
                    a.message_man = user.id
                    a.message_content = '欢迎登陆'
                    a.save()
                    url = request.COOKIES.get('url', '/')
                    ret = redirect(url)
                    ret.delete_cookie('url')
                    return ret
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


# def user_login(request):
#     if request.method == 'GET':
#         return render(request, 'users/login.html')
#     else:
#         user_login_form = UserLoginForm(request.POST)
#         if user_login_form.is_valid():
#             email = user_login_form.cleaned_data['email']
#             password = user_login_form.cleaned_data['password']
#
#             user = authenticate(username=email, password=password)
#             if user:
#                 if user.is_start:
#                     login(request, user)
#                     # 当登录成功,刷新一条消息
#                     a = UserMessage()
#                     a.message_man = user.id
#                     a.message_content = '欢迎登陆'
#                     a.save()
#                     url = request.COOKIES.get('url', '/')
#                     ret = redirect(url)
#                     ret.delete_cookie('url')
#                     return ret
#                 else:
#                     return HttpResponse('请前往您的邮箱进行激活,否则无法登录')
#             else:
#                 return render(request, 'users/login.html', {
#                     'msg': '邮箱或密码错误'
#                 })
#         else:
#             return render(request, 'users/login.html', {
#                 'user_login_form': user_login_form
#             })

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))

# def user_logout(request):
#     # if request.method == 'GET':
#     # return render(request, 'logout.html')
#     logout(request)
#     return redirect(reverse('index'))


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
                    # # 清除之前已经存在的验证码
                    # email_ver.delete()
                    return JsonResponse({'status': 'ok', 'msg': '请尽快到邮箱中获取验证码'})
                else:
                    return JsonResponse({'status': 'fail', 'msg': '请不要重复发送验证码'})
            else:
                send_email_code(email, 3)
                return JsonResponse({'status': 'ok', 'msg': '请尽快到邮箱中获取验证码'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '您输入的邮箱有误'})


def user_resetemail(request):
    user_resetemail_form = UserResetEmailForm(request.POST)
    if user_resetemail_form.is_valid():
        email = user_resetemail_form.cleaned_data['email']
        code = user_resetemail_form.cleaned_data['code']

        email_ver_list = EmailVerifyCode.objects.filter(email=email, code=code)
        if email_ver_list:
            email_ver = email_ver_list[0]
            if (datetime.now()-email_ver.add_time).seconds < 60:
                request.user.username = email
                request.user.email = email
                request.user.save()
                return JsonResponse({'status': 'ok', 'msg': '邮箱修改成功'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '验证码失效.请重新发送验证码'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '邮箱或者验证码有误'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '邮箱或者验证码不合法'})


def user_course(request):
    usercourse_list = request.user.usercourse_set.all()
    course_list = [usercourse.study_course for usercourse in usercourse_list]
    return render(request, 'users/usercenter_mycourse.html', {
        'course_list': course_list
    })


def user_loveorg(request):
    # userloveorg_list = request.user.userlove.all().filter(love_type=1)
    userloveorg_list = UserLove.objects.filter(love_man=request.user, love_type=1, love_status=True)
    org_ids = [userloveorg.love_id for userloveorg in userloveorg_list]
    org_list = OrgInfo.objects.filter(id__in=org_ids)
    return render(request, 'users/usercenter_fav_org.html', {
        'org_list': org_list,
    })


def user_loveteacher(request):
    userloveteacher_list = UserLove.objects.filter(love_man=request.user, love_type=3, love_status=True)
    teacher_ids = [userloveteacher.love_id for userloveteacher in userloveteacher_list]
    teacher_list = TeacherInfo.objects.filter(id__in=teacher_ids)
    return render(request, 'users/usercenter_fav_teacher.html', {
        'teacher_list': teacher_list,
    })


def user_lovecourse(request):
    userlovecourse_list = UserLove.objects.filter(love_man=request.user, love_type=3, love_status=True)
    course_ids = [userloveteacher.love_id for userloveteacher in userlovecourse_list]
    course_list = CourseInfo.objects.filter(id__in=course_ids)
    return render(request, 'users/usercenter_fav_course.html', {
        'course_list': course_list,
    })


def user_message(request):
    msg_list = UserMessage.objects.filter(message_man=request.user.id)
    return render(request, 'users/usercenter_message.html', {
        'msg_list': msg_list,

    })


def user_deletemessage(request):
    # 获取delete_id 参数,拿不到则给空值
    delete_id = request.GET.get('delete-id', '')
    if delete_id:
        msg = UserMessage.objects.filter(id = int(delete_id))[0]
        msg.message_status = True
        msg.save()
