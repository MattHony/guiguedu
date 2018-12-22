from django.core.paginator import Paginator, PageNotAnInteger
from django.core.paginator import EmptyPage
from django.shortcuts import render

# Create your views here.
from courses.models import CourseInfo
from operations.models import UserLove


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
        return render(request, 'courses/course_video.html', {
            'course': course,
        })
