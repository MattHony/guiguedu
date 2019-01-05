from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import render

from operations.models import UserLove
from .models import OrgInfo
from .models import CityInfo
from .models import TeacherInfo
# Create your views here.


def org_list(request):
    all_orgs = OrgInfo.objects.all()
    all_cities = CityInfo.objects.all()
    sort_orgs = all_orgs.order_by('-love_num')[:3]

    # 联合筛选
    # 按照机构类别进行过滤筛选
    cate = request.GET.get('cate', '')
    if cate:
        all_orgs = all_orgs.filter(category=cate)
    # 按照所在地区进行过滤筛选
    cityid = request.GET.get(('cityid', ''))
    if cityid:
        all_orgs = all_orgs.filter(cityinfo_id=int(cityid))

    # 排序 综合排序
    sort = request.GET.get('sort', '')
    if sort:
        # all_orgs = all_orgs.order_by('-'+sort)
        all_orgs = all_orgs.order_by(sort).reverse()

    # 分页
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_orgs, 3)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'orgs/org_list.html', {
        'all_orgs': all_orgs,
        'all_cities': all_cities,
        'pages': pages,
        'sort_orgs': sort_orgs,
        'cate': cate,
        'cityid': cityid,
        'sort': sort,
    })


def org_detail(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]

        org.click_num += 1
        org.save()

        return render(request, 'orgs/org_detail_homepage.html', {
            'org': org,
            'detail_type': 'home'
        })


def org_detail_course(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        all_courses = org.courseinfo_set.all()

        # 分页
        pagenum = request.GET.get('pagenum', '')
        pa = Paginator(all_courses, 2)
        try:
            pages = pa.page(pagenum)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        return render(request, 'orgs/org_detail_course.html', {
            'org': org,
            'pages': pages,
            'detail_type': 'course',
        })


def org_detail_desc(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        return render(request, 'orgs/org_detail_desc.html', {
            'org': org,
            'detail_type': 'desc',
        })


def org_detail_teacher(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        return render(request, 'orgs/org_detail_teachers.html', {
            'org': org,
            'detail_type': 'teacher',
        })


def teacher_list(request):
    all_teachers = TeacherInfo.objects.all()
    sort_teachers = all_teachers.order_by('-love_num')[:2]

    sort = request.GET.get('sort', '')
    if sort:
        all_teachers = all_teachers.order_by('-'+sort)

    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_teachers, 2)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'orgs/teachers_list.html', {
        'all_teachers': all_teachers,
        'sort_teachers': sort_teachers,
        'pages': pages,
        'sort': sort
    })


def teacher_detail(request, teacher_id):
    if teacher_id:
        all_teachers = TeacherInfo.objects.all()
        teacher = TeacherInfo.objects.filter(id = int(teacher_id))[0]
        sort_teachers = all_teachers.order_by('-love_num')[:2]

        teacher.click_num += 1
        teacher.save()

        # lovecourse和loveorg 用于存储用户收藏的状态,在模板中
        # 根据这个状态来确定页面加载时,显示的是收藏还是取消收藏
        loveteacher = False
        loveorg = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_id=int(teacher_id), love_type=3, love_status=True, love_man=request.user)
            if love:
                loveteacher = True
            love1 = UserLove.objects.filter(love_id=teacher.work_company.id, love_type=1, love_status=True,
                                            love_man=request.user)
            if love1:
                loveorg = True
        return render(request, 'orgs/teacher_detail.html', {
            'teacher': teacher,
            'sort_teachers': sort_teachers,
            'loveteacher': loveteacher,
            'loveorg': loveorg,
        })