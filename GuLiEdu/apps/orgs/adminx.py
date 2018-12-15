import xadmin

from .models import *


class CityInfoXadmin(object):
    list_display = ['name', 'add_time']
    model_icon = 'fa fa-tag'


class OrgInfoXadmin(object):
    list_display = ['image', 'name', 'course_num', 'learn_num', 'love_num', 'click_num', 'category', 'cityinfo',
                    'add_time']
    model_icon = 'fa fa-tag'


class TeacherInfoXadmin(object):
    list_display = ['image', 'name', 'work_year', 'work_style', 'work_position', 'click_num', 'love_num',
                    'add_time', 'gender']
    model_icon = 'fa fa-tag'


xadmin.site.register(CityInfo, CityInfoXadmin)
xadmin.site.register(OrgInfo, OrgInfoXadmin)
xadmin.site.register(TeacherInfo, TeacherInfoXadmin)
