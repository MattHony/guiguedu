from django.http import JsonResponse

# Create your views here.
from operations.forms import UserAskForm, UserCommentForm
from operations.models import UserLove, UserComment
from orgs.models import OrgInfo, TeacherInfo
from courses.models import CourseInfo


def user_ask(request):
    user_ask_form = UserAskForm(request.POST)
    if user_ask_form.is_valid():
        # 这里使用forms.ModelForm  form表单和model数据表均保存
        user_ask_form.save(commit=True)

        # form表单使用forms.Form继承
        # name = user_ask_form.cleaned_data['name']
        # phone = user_ask_form.cleaned_data['phone']
        # course = user_ask_form.cleaned_data['course']
        #
        # a = UserAsk()
        # a.name = name
        # a.phone = phone
        # a.course = course
        # a.save()
        return JsonResponse({'status': 'ok', 'msg': '咨询成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '咨询失败'})


def user_love(request):
    loveid = request.GET.get('loveid', '')
    lovetype = request.GET.get('lovetype', '')
    if loveid and lovetype:
        # 根据传递的收藏类型,判断是什么对象
        # 根据传递的收藏ID,判断收藏是哪一个对象
        obj = None
        if int(lovetype) == 1:
            obj = OrgInfo.objects.filter(id=int(loveid))[0]
        elif int(lovetype) == 2:
            obj = CourseInfo.objects.filter(id=int(loveid))[0]
        elif int(lovetype) == 3:
            obj = TeacherInfo.objects.filter(id=int(loveid))[0]

        # 收藏的id和type同时存在,就去收藏表当中去查找有没有这个用户的收藏记录
        love = UserLove.objects.filter(love_id=str(loveid), love_type=str(lovetype), love_man=request.user)
        if love:
            # 判断收藏记录,如果收藏记录为真,则代表之前收藏过,现在页面显示
            # 的应为取消收藏,表示本次点击为取消收藏
            if love[0].love_status:
                love[0].love_status = False
                love[0].save()
                obj.love_num -= 1
                obj.save()

                return JsonResponse({'status': 'ok', 'msg': '收藏'})
            else:
                love[0].love_status = True
                love[0].save()
                obj.love_num += 1
                obj.save()
                return JsonResponse({
                    'status': 'OK',
                    'msg': '取消收藏',
                })
        else:
            # 之前没有收藏过这个东西,创建收藏记录,再把这个记录的状态改为True
            a = UserLove()
            a.love_man = request.user
            a.love_id = int(loveid)
            a.love_type = int(lovetype)
            a.love_status = True
            a.save()
            obj.love_num += 1
            obj.save()
            return JsonResponse({
                'status': 'OK',
                'msg': '取消收藏',
            })
    else:
        return JsonResponse({'status': 'fail', 'msg': '收藏失败'})


def user_comment(request):
    user_comment_form = UserCommentForm(request.POST)
    if user_comment_form.is_valid():
        comment_course = user_comment_form.cleaned_data['comment_course']
        comment_content = user_comment_form.cleaned_data['comment_content']
        a = UserComment()
        a.comment_content = comment_content
        a.comment_man = request.user
        a.comment_course_id = comment_course
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '评论成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '评论失败'})
