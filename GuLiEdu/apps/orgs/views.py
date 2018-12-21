from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import OrgInfo
from .models import CityInfo
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