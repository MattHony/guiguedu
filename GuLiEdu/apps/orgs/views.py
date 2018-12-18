from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import OrgInfo
from .models import TeacherInfo
from .models import CityInfo
# Create your views here.


def org_list(request):
    all_orgs = OrgInfo.objects.all()
    all_cities = CityInfo.objects.all()
    sort_orgs = all_orgs.order_by('-love_num')[:3]

    # 分页
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_orgs, 3)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'org_list.html', {
        'all_orgs': all_orgs,
        'all_cities': all_cities,
        'pages': pages,
        'sort_orgs': sort_orgs
    })