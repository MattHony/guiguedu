from django.shortcuts import render

from .models import OrgInfo
from .models import TeacherInfo
from .models import CityInfo
# Create your views here.


def org_list(request):
    all_orgs = OrgInfo.objects.all()
    return render(request, 'org_list.html', {
        'all_orgs': all_orgs
    })