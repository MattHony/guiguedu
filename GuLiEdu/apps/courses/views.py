from django.core.paginator import Paginator, PageNotAnInteger
from django.core.paginator import EmptyPage
from django.shortcuts import render

# Create your views here.
from courses.models import CourseInfo
from operations.models import UserLove, UserCourse


def course_list(request):
    all_courses = CourseInfo.objects.all()
    recommend_courses = all_courses.order_by('-add_time')[:3]

    sort = request.GET.get('sort', '')
    if sort:
        all_courses = all_courses.order_by(sort).reverse()

    # 分页
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_courses, 2)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'courses/course_list.html', {
        'all_courses': all_courses,
        'pages': pages,
        "recommend_courses": recommend_courses,
        'sort': sort,
    })


def course_detail(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        # 相关课程推荐 除去课程本身的course_id exclude()
        related_course = CourseInfo.objects.filter(category=course.category).exclude(id=int(course_id))[:2]

        # lovecourse和loveorg 用于存储用户收藏的状态,在模板中
        # 根据这个状态来确定页面加载时,显示的是收藏还是取消收藏
        lovecourse = False
        loveorg = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_id=int(course_id), love_type=2, love_status=True, love_man=request.user)
            if love:
                lovecourse = True
            love = UserLove.objects.filter(love_id=course.orginfo.id, love_type=1, love_status=True,
                                           love_man=request.user)
            if love:
                loveorg = True

        return render(request, 'courses/course_list.html', {
            'course': course,
            'related_course': related_course,
            'lovecourse': lovecourse,
            'loveorg': loveorg,
        })


def course_video(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]

        # 点击开始学习,代表用户学习了这个课程
        usercourse_list = UserCourse.objects.filter(study_man=request.user, study_course=course)
        if not usercourse_list:
            a = UserCourse()
            a.study_man = request.user
            a.study_course = course
            a.save()

            # 学过该课程同学还学过课程功能
            # 1: 从所有对象中获取到学习该课程的所有对象
            usercourse_list = UserCourse.objects.filter(study_course=course)

            # 2: 根据找到的用户学习课程列表,遍历拿到所有学习过这门课程的用户列表  列表生成式 而非append
            user_list = [usercourse.study_man for usercourse in usercourse_list]

            # 3: 再根据找到的用户,从用户学习课程表当中,找到所有用户学习其他课程的整个对象 使用exclude除去当前学过的这个课程对象
            usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)

            # 4: 从获取到的用户课程列表中,拿到我们需要的其他课程
            course_list = list(set([usercourse.study_course for usercourse in usercourse_list]))

            return render(request, 'courses/course_video.html',
                          {'course': course,
                           'course_list': course_list
                           })


def course_comment(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        all_comments = course.usercomment_set.all()[:10]

        # 学过该课程同学还学过课程功能
        # 1: 从所有对象中获取到学习该课程的所有对象
        usercourse_list = UserCourse.objects.filter(study_course=course)

        # 2: 根据找到的用户学习课程列表,遍历拿到所有学习过这门课程的用户列表  列表生成式 而非append
        user_list = [usercourse.study_man for usercourse in usercourse_list]

        # 3: 再根据找到的用户,从用户学习课程表当中,找到所有用户学习其他课程的整个对象 使用exclude除去当前学过的这个课程对象
        usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)

        # 4: 从获取到的用户课程列表中,拿到我们需要的其他课程
        course_list = list(set([usercourse.study_course for usercourse in usercourse_list]))

        return render(request, 'courses/course_comment.html', {
            'course': course,
            'all_comments': all_comments,
            'course_list': course_list,
        })
